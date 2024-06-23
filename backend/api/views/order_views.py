from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from api.models import Order
from api.serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination
from api.renderers import CustomJSONRenderer
from rest_framework.exceptions import NotFound
# This class defines a custom pagination style for the OrderListView and OrderDetailView
class StandardResultsSetPagination(PageNumberPagination):
    # The number of items to display per page
    page_size = 10
    # The query parameter to use for specifying the page size
    page_size_query_param = 'page_size'
    # The maximum allowed page size
    max_page_size = 1000

# This class defines an API view for listing all orders
class OrderListView(APIView):
    # The permission classes required to access this view
    permission_classes = [IsAuthenticated, IsAdminUser]
    # The renderer classes to use for serializing the response
    renderer_classes = [CustomJSONRenderer]
    
    # This method retrieves all orders and paginates them, returning the serialized data
    def get(self, request):
        # Retrieve all orders and order them by the order date in descending order
        orders = Order.objects.all().order_by('-order_date')
        # Create an instance of the pagination class
        paginator = StandardResultsSetPagination()
        # Paginate the orders based on the request
        paginated_orders = paginator.paginate_queryset(orders, request)
        # Serialize the paginated orders
        serializer = OrderSerializer(paginated_orders, many=True)
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)

    # This method creates a new order and returns the serialized data
    def post(self, request):
        # Create a serializer instance with the request data
        serializer = OrderSerializer(data=request.data)
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Save the serialized data with the authenticated user
            serializer.save(user=request.user)
            # Return the serialized data with a 201 Created status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return the serializer errors with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This class defines an API view for retrieving, updating, and deleting a specific order
class OrderDetailView(APIView):
    # The permission classes required to access this view
    permission_classes = [IsAuthenticated, IsAdminUser]
    # The renderer classes to use for serializing the response
    renderer_classes = [CustomJSONRenderer]

    # This method retrieves an order by its primary key and raises an exception if it doesn't exist
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound('Order not found')
    
    # This method retrieves an order by its primary key and returns the serialized data
    def get(self, request, pk):
        # Retrieve the order by its primary key
        order = self.get_object(pk)
        # Serialize the order
        serializer = OrderSerializer(order)
        # Return the serialized data
        return Response(serializer.data)

    # This method updates an order by its primary key and returns the serialized data
    def put(self, request, pk):
        # Retrieve the order by its primary key
        order = self.get_object(pk)
        # Create a serializer instance with the request data
        serializer = OrderSerializer(order, data=request.data)
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Save the serialized data
            serializer.save()
            # Return the serialized data
            return Response(serializer.data)
        # Return the serializer errors with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # This method deletes an order by its primary key and returns a 204 No Content status code
    def delete(self, request, pk):
        # Retrieve the order by its primary key
        order = self.get_object(pk)
        # Delete the order
        order.delete()
        # Return a 204 No Content status code
        return Response(status=status.HTTP_204_NO_CONTENT)
