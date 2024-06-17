from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
from api.models import Product
from api.serializers import ProductSerializer,Review,ReviewSerializer
from rest_framework.permissions import IsAdminUser
from api.renderers import CustomJSONRenderer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    
    def get(self, request):
        query = request.query_params.get('keyword', '')
        products = Product.objects.filter(name__icontains=query).order_by('-id')
        
        paginator = StandardResultsSetPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class TopProductsView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        products = Product.objects.filter(rating__gte=4).order_by('-rating')[:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class CreateProductReviewView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    renderer_classes = [CustomJSONRenderer]

    def post(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        data = request.data
        
        # Check if user has already reviewed the product
        already_exists = product.reviews.filter(user=user).exists()
        if already_exists:
            return Response({'detail': 'Product already reviewed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create review
        review = Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
