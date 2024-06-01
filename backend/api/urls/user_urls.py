from django.urls import path,include
from api.views import user_views as views
urlpatterns = [
    path('register/',views.RegisterUser,name='register'),
    path()
]
