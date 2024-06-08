# This file contains the URL mappings for the user views.
# The URLs defined here are used to map the user views to the corresponding URLs.

# Import the necessary modules
from django.urls import path, include  # Import the path and include functions from the django.urls module

# Import the TokenRefreshView & TokenObtainPairView from the rest_framework_simplejwt.views module
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView  

# Import the user views
from api.views.user_views import *  # Import the user views from the api.views.user_views module

# Define the URL patterns
urlpatterns = [
    
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Map the '/register/' URL to the RegisterView
    path('register/', RegisterView.as_view()),  # Map the URL to the RegisterView.as_view() function
    
    # Map the '/login/' URL to the LoginView
    path('login/', LoginView.as_view()),  # Map the URL to the LoginView.as_view() function
    
    # Map the '/profile/' URL to the UserView
    path('profile/', UserView.as_view()),  # Map the URL to the UserView.as_view() function
    
    # Map the '/logout/' URL to the LogoutView
    path('logout/', LogoutView.as_view()), # Map the URL to the LogoutView.as_view() function
     
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
    
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'), 
]

