from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Cart, CartItem, Product
from api.serializers import CartSerializer, CartItemSerializer
from api.renderers import CustomJSONRenderer
from rest_framework.exceptions import NotFound, ValidationError

# This class defines the API endpoints for the shopping cart.
class CartListView(APIView):
    # Specify the permission class for the API endpoints.
    permission_classes = [IsAuthenticated]
    # Specify the renderer class for the API endpoints.
    renderer_classes = [CustomJSONRenderer]

    # GET method for the API endpoint. Retrieves the cart for the authenticated user.
    def get(self, request):
        # Get or create the cart for the authenticated user.
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Serialize the cart data into JSON format.
        serializer = CartSerializer(cart)
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST method for the API endpoint. Adds a product to the cart for the authenticated user.
    def post(self, request):
        # Get or create the cart for the authenticated user.
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Get the product data from the request.
        data = request.data
        # Get the product with the specified ID. Raise a 404 error if the product is not found.
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        # Get or create the cart item for the product in the cart.
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': data['quantity']}
        )
        
        # If the cart item already exists, increment the quantity.
        if not created:
            cart_item.quantity += data['quantity']
            cart_item.save()

        # Serialize the cart item data into JSON format.
        serializer = CartItemSerializer(cart_item)
        # Return the serialized data as the response with a 201 Created status code.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# This class defines the API endpoints for a specific cart item in the shopping cart.
class CartItemDetailView(APIView):
    # Specify the permission class for the API endpoints.
    permission_classes = [IsAuthenticated]
    # Specify the renderer class for the API endpoints.
    renderer_classes = [CustomJSONRenderer]

    # Helper method to get the cart item for the authenticated user and the specified primary key.
    def get_object(self, pk, user):
        try:
            # Get the cart item with the specified primary key and the user's cart.
            return CartItem.objects.get(pk=pk, cart__user=user)
        except CartItem.DoesNotExist:
            # Raise a 404 error if the cart item is not found.
            raise NotFound('Cart item not found')

    # GET method for the API endpoint. Retrieves the cart item for the authenticated user and the specified primary key.
    def get(self, request, pk):
        # Get the cart item for the authenticated user and the specified primary key.
        cart_item = self.get_object(pk, request.user)
        # Serialize the cart item data into JSON format.
        serializer = CartItemSerializer(cart_item)
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT method for the API endpoint. Updates the cart item for the authenticated user and the specified primary key.
    def put(self, request, pk):
        # Get the cart item for the authenticated user and the specified primary key.
        cart_item = self.get_object(pk, request.user)
        # Serialize the cart item data into JSON format with the updated data from the request.
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        # Validate the serialized data. If it's not valid, raise an exception.
        serializer.is_valid(raise_exception=True)
        # Save the validated data to the database.
        serializer.save()
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE method for the API endpoint. Deletes the cart item for the authenticated user and the specified primary key.
    def delete(self, request, pk):
        # Get the cart item for the authenticated user and the specified primary key.
        cart_item = self.get_object(pk, request.user)
        # Delete the cart item from the database.
        cart_item.delete()
        # Return an empty response with a 204 No Content status code.
        return Response(status=status.HTTP_204_NO_CONTENT)

