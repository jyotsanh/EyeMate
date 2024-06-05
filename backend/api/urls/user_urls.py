from django.urls import path,include
from api.views.user_views import RegisterView,LoginView,UserView,LogoutView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('authenticate/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
]
