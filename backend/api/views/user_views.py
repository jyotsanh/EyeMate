from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import UserSerializer
from api.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from api.renderers import CustomJSONRenderer  # Import your custom renderer
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin


# RegisterView: This class handles the registration of a new user by accepting a POST request.
# It uses the UserSerializer to validate the data and create a new User object.
# It then generates a refresh token for the user and returns it along with the user details.
class RegisterView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        # Deserialize the request data into a UserSerializer object
        serializer = UserSerializer(data=request.data)
        # Check if the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        # Save the user to the database
        user = serializer.save()

        # Generate a refresh token for the user
        refresh = RefreshToken.for_user(user)
        # Get the access token from the refresh token
        access_token = refresh.access_token

        # Return the user details, access token, and refresh token as a response
        return Response({
            'user': serializer.data,
            'access': str(access_token),
            'refresh': str(refresh),
        })

# LoginView: This class handles the login of a user by accepting a POST request.
# It authenticates the user using the provided email and password.
# If the authentication is successful, it generates a refresh token for the user and returns it.
class LoginView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        # Get the email and password from the request data
        email = request.data['email']
        password = request.data['password']
        # Authenticate the user using the provided credentials
        user = authenticate(email=email, password=password)
        
        # If the user authentication fails, raise an exception
        if user is None:
            raise AuthenticationFailed('Invalid credentials!')

        # Generate a refresh token for the user
        refresh = RefreshToken.for_user(user)
        # Get the access token from the refresh token
        access_token = refresh.access_token

        # Return the access token and refresh token as a response
        return Response({
            'access': str(access_token),
            'refresh': str(refresh),
        })

# UserView: This class handles getting the details of an authenticated user by accepting a GET request.
# It requires the user to be authenticated and uses the JWTAuthentication class for authentication.
# It returns the user details as a response.
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        # Get the authenticated user from the request
        user = request.user
        # Serialize the user object
        serializer = UserSerializer(user)
        # Return the serialized user data as a response
        return Response(serializer.data)

# LogoutView: This class handles the logout of a user by accepting a POST request.
# It requires the user to be authenticated and uses the JWTAuthentication class for authentication.
# It blacklists the provided refresh token, making it unusable.
# It returns a success message as a response.
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data['refresh_token']
            # Create a RefreshToken object from the refresh token
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token, making it unusable
            token.blacklist()
            # Return a success message as a response
            return Response({'message': 'Success'})
        except Exception as e:
            # If an exception occurs, return the exception message as a response with a 400 status code
            return Response({'message': str(e)}, status=400)

# DeleteUserView: This class handles deleting an authenticated user by accepting a DELETE request.
# It requires the user to be authenticated and uses the JWTAuthentication class for authentication.
# It deletes the user from the database and returns a success message as a response.
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Use the custom permission here
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def delete(self, request):
        # Get the authenticated user from the request
        user = request.user
        # Delete the user from the database
        user.delete()
        # Return a success message as a response
        return Response({'message': 'User deleted successfully'})

# ResetPasswordView: This class handles resetting the password of an authenticated user by accepting a POST request.
# It requires the user to be authenticated and uses the JWTAuthentication class for authentication.
# It sets the new password for the user and returns a success message as a response.
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        # Get the authenticated user from the request
        user = request.user
        # Get the new password from the request data
        new_password = request.data.get('new_password')
        # If no new password is provided, return an error response
        if not new_password:
            return Response({'message': 'New password not provided'}, status=400)
        # Set the new password for the user
        user.set_password(new_password)
        user.save()
        # Return a success message as a response
        return Response({'message': 'Password reset successfully'})

# UserUpdateView: This class handles updating the details of an authenticated user by accepting a PATCH request.
# It requires the user to be authenticated and uses the JWTAuthentication class for authentication.
# It updates the user details with the provided data and returns the updated user details as a response.
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Use the custom permission here
    authentication_classes = [JWTAuthentication]
    renderer_classes = [CustomJSONRenderer]

    def patch(self, request):
        # Get the authenticated user from the request
        user = request.user
        # Deserialize the request data into a UserSerializer object
        serializer = UserSerializer(user, data=request.data, partial=True)
        # Check if the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        # Save the updated user to the database
        serializer.save()
        # Return the updated user details as a response
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Get the authenticated user from the request
        user = request.user
        # Deserialize the request data into a UserSerializer object
        serializer = UserSerializer(user, data=request.data)
        # Check if the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        # Save the updated user to the database
        serializer.save()
        # Return the updated user details as a response
        return Response(serializer.data, status=status.HTTP_200_OK)