# This file contains the implementation of the views for user registration, login, user details retrieval, and logout.

# Import necessary modules
from rest_framework.views import APIView  # Import the APIView base class from the rest_framework module
from api.serializers import UserSerializer  # Import the UserSerializer class from the api.serializers module
from rest_framework.response import Response  # Import the Response class from the rest_framework.response module
from api.models import User  # Import the User model from the api.models module
from rest_framework.exceptions import AuthenticationFailed  # Import the AuthenticationFailed exception class
import jwt  # Import the jwt module
import datetime  # Import the datetime module

# RegisterView class inherits from the APIView base class and handles the user registration functionality
class RegisterView(APIView):
    def post(self,request):
        # Serialize the request data using the UserSerializer
        serializer = UserSerializer(data=request.data)
        # Validate the serialized data
        serializer.is_valid(raise_exception=True)
        # Save the validated data to the database
        serializer.save()
        # Return the serialized data as the response
        return Response(serializer.data)
    
# LoginView class inherits from the APIView base class and handles the user login functionality
class LoginView(APIView):
    def post(self,request):
        # Extract the email and password from the request data
        email = request.data['email']
        password = request.data['password']

        # Retrieve the user from the database based on the email
        user = User.objects.filter(email=email).first()

        # If the user is not found, raise an AuthenticationFailed exception
        if user is None:
            raise AuthenticationFailed('User not found!') 
        # If the provided password does not match the user's password, raise an AuthenticationFailed exception
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')  
        
        # Generate the payload for the JWT token
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),  # Set the expiration time of the token
            'iat':datetime.datetime.utcnow()  # Set the issued at time of the token
        }

        # Generate the JWT token using the payload and the 'secret' key
        token = jwt.encode(payload,'secret',algorithm='HS256')

        # Create a response object
        response = Response()
        # Set the 'jwt' cookie in the response with the generated token
        response.set_cookie(key='jwt',value=token,httponly=True)
        # Set the data of the response to the generated token
        response.data = {
            'jwt':token
        }
        
        # Return the response
        return response
    
# UserView class inherits from the APIView base class and handles the user details retrieval functionality
class UserView(APIView):
    def get(self,request):
        # Retrieve the 'jwt' cookie from the request
        token = request.COOKIES.get('jwt')   

        # If the token is not present, raise an AuthenticationFailed exception
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode the token using the 'secret' key
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # If the token has expired, raise an AuthenticationFailed exception
            raise AuthenticationFailed('Unauthenticated!')

        # Retrieve the user from the database based on the user id in the payload
        user = User.objects.filter(id=payload['id']).first()
        # Serialize the user object using the UserSerializer
        serializer = UserSerializer(user)

        # Return the serialized user object as the response
        return Response(serializer.data)
    
# LogoutView class inherits from the APIView base class and handles the logout functionality
class LogoutView(APIView):
    def post(self,request):
        # Create a response object
        response = Response()
        # Delete the 'jwt' cookie from the response
        response.delete_cookie('jwt')
        # Set the data of the response to a success message
        response.data = {
            'message':'success'
        }
        # Return the response
        return response
