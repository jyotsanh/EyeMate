from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Product
from api.serializers import ProductSerializer,Review,ReviewSerializer,TopProductsSerializer
from rest_framework.permissions import IsAdminUser
from api.renderers import CustomJSONRenderer
from django.db.models import Q
from django.db.models import Avg


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4 
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    
    def get(self, request):
        query = request.query_params.get('keyword', '') 
        search_filter = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
        products = Product.objects.filter(search_filter).order_by('id') 
        paginator = StandardResultsSetPagination() 
        paginated_products = paginator.paginate_queryset(products, request) 
        
        # Check if paginated_products is None
        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            data = serializer.data
        else:
            
            data = []
        next_link = paginator.get_next_link() if paginator.get_next_link() else ''
        previous_link = paginator.get_previous_link() if paginator.get_previous_link() else ''
        
        response_data = {
            'results': data,
            'count': paginator.page.paginator.count if paginated_products is not None else 0,
            'next': next_link,
            'previous': previous_link
        } 
        return Response(response_data)
class TopProductsView(APIView):
    renderer_classes = [CustomJSONRenderer]
    def get(self, request, format=None):
        products = Product.objects.annotate(average_rating=Avg('reviews__rating')).filter(average_rating__gte=4).order_by('-average_rating')[:6]
        serializer = TopProductsSerializer(products, many=True)
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
