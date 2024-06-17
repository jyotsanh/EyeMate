from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/',include('api.urls.product_urls')),
    path('api/user/',include('api.urls.user_urls')),
    path('api/orders/',include('api.urls.order_urls')),
    path('api/cart/',include('api.urls.cart_urls')),
    path('api/review/',include('api.urls.review_urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # for development only
# still both urlpatterns needs to understand
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) # for development only