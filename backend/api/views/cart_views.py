from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Cart, CartItem, Product
from api.serializers import CartSerializer, CartItemSerializer
from api.renderers import CustomJSONRenderer
from rest_framework.exceptions import NotFound, ValidationError

class CartListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        data = request.data
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': data['quantity']}
        )
        
        if not created:
            cart_item.quantity += data['quantity']
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get_object(self, pk, user):
        try:
            return CartItem.objects.get(pk=pk, cart__user=user)
        except CartItem.DoesNotExist:
            raise NotFound('Cart item not found')

    def get(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
