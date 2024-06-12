# This file contains the URL mappings for the user views.
# The URLs defined here are used to map the user views to the corresponding URLs.

# Import the necessary modules
from django.urls import path, include  # Import the path and include functions from the django.urls module

# Import the user views
from api.views.user_views import *  # Import the user views from the api.views.user_views module

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-login-otp/', OTPLoginVerifyView.as_view(), name='verify-login-otp'),
    path('profile/', UserView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('verify-reset-password/', VerifyResetPasswordView.as_view(), name='verify-reset-password'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('update-user/', UserUpdateView.as_view(), name='update-user'),
]
