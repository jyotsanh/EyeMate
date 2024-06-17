from django.urls import path,include
from api.views.cart_views import *

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart_item_detail'),
]