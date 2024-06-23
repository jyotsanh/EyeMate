from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import random
from rest_framework.permissions import BasePermission
from api.models import User
from api.otp import OTP # Import the OTP model from otp.py
import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


from api.serializers import (
    UserSerializer,
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer, 
    OTPVerifySerializer
) # all the serializers class from serialzers.py
from api.renderers import CustomJSONRenderer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class IsAdminUser(BasePermission): # checks if the user is an admin or not
    def has_permission(self, request, view):
        return request.user and request.user.is_admin 

class RegisterView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        response = Response(
            {"msg": "Registration successful"},
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response


class LoginView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"errors": {"non_field_errors": ["Email or password is not valid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
        token = get_tokens_for_user(user)

        response = Response({"msg": "Log-in Successful"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=token['refresh'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='access_token',
            value=token['access'],
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        return response

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"message": "Success"})
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        user = request.user # get the logged in user
        otp_code = str(random.randint(100000, 999999)) # Creates a OTP of 6 digit
        
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'lalalallalaop67@gmail.com',
            [user.email], # get user email address to send otp
            fail_silently=False,
        )

        return Response(
            {
                'msg': 'OTP sent to your email. Please verify to continue.'
            },status=status.HTTP_200_OK
            )

class VerifyResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # checks if each data is provide or not

        otp_code_recieved = serializer.validated_data['otp_code'] # get the otp code
        
        user = request.user
        otp = OTP.objects.filter(
                                    user=user, # get the otp of logged in user
                                    otp_code=otp_code_recieved, # check if the otp code is valid
                                    used=False # check if the otp is not used
                                ).first()
        
        if otp is None or otp.is_expired(): # check if otp is expired or exist or not.
            return Response(
                {
                    'errors': {
                        'otp_code': ['Invalid or expired OTP']
                        }
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        
        otp.used = True # set the used = True if the otp is availabel in table and not expired
        otp.save() # save the otp
        
        new_password = serializer.validated_data['new_password'] # get the new password
        if not new_password:
            return Response(
                {
                    'message': 'New password not provided'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        
        user.password = make_password(new_password) # hash of new pswd
        user.save() # save the user
        
        return Response(
            {
                'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK
            )

@permission_classes([IsAdminUser])
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {
                'message': 'User deleted successfully'
            }, status=status.HTTP_200_OK
            )

@permission_classes([IsAdminUser])
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)