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


# This class defines a custom pagination style for the ProductListView API view
class StandardResultsSetPagination(PageNumberPagination):
    # Specify the number of items to display per page
    page_size = 4 
    # Specify the name of the query parameter used to specify the page size
    page_size_query_param = 'page_size'
    # Specify the maximum allowed page size
    max_page_size = 1000


# This API view handles GET requests to retrieve a list of products
class ProductListView(APIView):
    # Specify the renderer class to use for serializing the response data
    renderer_classes = [CustomJSONRenderer]
    
    # Define the logic for handling GET requests
    def get(self, request):
        # Get the search keyword from the query parameters
        query = request.query_params.get('keyword', '') 
        # Define a filter to search for products based on the keyword
        search_filter = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
        # Retrieve all products that match the filter and order them by ID
        products = Product.objects.filter(search_filter).order_by('id') 
        # Create an instance of the paginator class
        paginator = StandardResultsSetPagination() 
        # Paginate the queryset based on the request
        paginated_products = paginator.paginate_queryset(products, request) 
        
        # Check if there are any paginated products
        if paginated_products is not None:
            # Serialize the paginated products
            serializer = ProductSerializer(paginated_products, many=True)
            data = serializer.data
        else:
            # If there are no paginated products, return an empty list
            data = []
        # Get the next and previous page links
        next_link = paginator.get_next_link() if paginator.get_next_link() else ''
        previous_link = paginator.get_previous_link() if paginator.get_previous_link() else ''
        
        # Create the response data
        response_data = {
            'results': data,
            'count': paginator.page.paginator.count if paginated_products is not None else 0,
            'next': next_link,
            'previous': previous_link
        } 
        # Return the response
        return Response(response_data)

# This API view handles GET requests to retrieve the top 6 products with an average rating of 4 or higher
class TopProductsView(APIView):
    renderer_classes = [CustomJSONRenderer]
    def get(self, request, format=None):
        # Retrieve the top 6 products with an average rating of 4 or higher, ordered by average rating in descending order
        products = Product.objects.annotate(
            average_rating = Avg('reviews__rating')
            ).filter(
                average_rating__gte = 4
                ).order_by('-average_rating')[:6]
        # Serialize the products
        serializer = TopProductsSerializer(products, many=True)
        # Return the serialized data as the response
        return Response(serializer.data)

# This API view handles GET requests to retrieve details of a specific product
class ProductDetailView(APIView):
    renderer_classes = [CustomJSONRenderer]
    def get(self, request, pk):
        try:
            # Retrieve the product with the specified primary key
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            # If the product does not exist, return a 404 error response
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        # Serialize the product
        serializer = ProductSerializer(product)
        # Return the serialized data as the response
        return Response(serializer.data)

# This API view handles POST requests to create a review for a specific product
class CreateProductReviewView(APIView):
    # Specify the permission classes required to access this view
    permission_classes = [IsAuthenticated, IsAdminUser]
    renderer_classes = [CustomJSONRenderer]

    # Define the logic for handling POST requests
    def post(self, request, pk):
        # Get the authenticated user and the product with the specified primary key
        user = request.user
        product = Product.objects.get(pk=pk)
        # Get the review data from the request
        data = request.data
        
        # Check if the user has already reviewed the product
        already_exists = product.reviews.filter(user=user).exists()
        if already_exists:
            # If the user has already reviewed the product, return a 400 error response
            return Response({'detail': 'Product already reviewed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new review for the product with the review data
        review = Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
        
        # Serialize the new review
        serializer = ReviewSerializer(review)
        # Return the serialized data as the response with a 201 Created status code
        return Response(serializer.data, status=status.HTTP_201_CREATED)

