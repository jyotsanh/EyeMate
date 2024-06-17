from django.urls import path,include
from api.views.order_views import *
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
