from django.urls import path,include
from api.views.product_views import *
urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/top/', TopProductsView.as_view(), name='top_products'),
    path('products/<int:pk>/reviews/', CreateProductReviewView.as_view(), name='create_product_review'),
]
