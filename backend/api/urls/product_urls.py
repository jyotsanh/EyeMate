from django.urls import path,include
from api.views.product_views import *
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('top', TopProductsView.as_view(), name='top_products'),
    path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/reviews', CreateProductReviewView.as_view(), name='create_product_review'),
]
