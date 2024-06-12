from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
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
from api.otp import OTP
import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


from api.serializers import (
    UserSerializer,
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer, 
    OTPVerifySerializer
)
from api.renderers import CustomJSONRenderer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin 

class RegisterView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'lalalallalaop67@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'msg': 'Registration successful. Please verify OTP sent to your email.'}, status=status.HTTP_201_CREATED)

class OTPVerifyView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        user = User.objects.get(email=email)
        otp = OTP.objects.filter(user=user, otp_code=otp_code, used=False).first()
        
        if otp is None or otp.is_expired():
            return Response({'errors': {'otp_code': ['Invalid or expired OTP']}}, status=status.HTTP_400_BAD_REQUEST)
        
        otp.used = True
        otp.save()
        
        token = get_tokens_for_user(user)

        return Response({'token': token, 'msg': 'OTP verified successfully'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response({'errors': {'non_field_errors': ['Invalid credentials']}}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'lalalallalaop67@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'msg': 'OTP sent to your email. Please verify to continue.'}, status=status.HTTP_200_OK)

class OTPLoginVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        user = User.objects.get(email=email)
        otp = OTP.objects.filter(user=user, otp_code=otp_code, used=False).first()
        
        if otp is None or otp.is_expired():
            return Response({'errors': {'otp_code': ['Invalid or expired OTP']}}, status=status.HTTP_400_BAD_REQUEST)
        
        otp.used = True
        otp.save()
        
        token = get_tokens_for_user(user)

        return Response({'token': token, 'msg': 'OTP verified successfully'}, status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Success'})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        user = request.user
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'lalalallalaop67@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'msg': 'OTP sent to your email. Please verify to continue.'}, status=status.HTTP_200_OK)

class VerifyResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        user = request.user
        otp = OTP.objects.filter(user=user, otp_code=otp_code, used=False).first()
        
        if otp is None or otp.is_expired():
            return Response({'errors': {'otp_code': ['Invalid or expired OTP']}}, status=status.HTTP_400_BAD_REQUEST)
        
        otp.used = True
        otp.save()
        
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'message': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(new_password)
        user.save()
        
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'})

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