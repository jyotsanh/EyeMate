from django.urls import path,include
from api.views.review_views import *

urlpatterns = [
     path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
]