from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Review, Product
from api.serializers import ReviewSerializer
from rest_framework.exceptions import NotFound, ValidationError
from api.renderers import CustomJSONRenderer

class ReviewListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        user = request.user
        product = Product.objects.get(id=product_id)
        if Review.objects.filter(product=product, user=user).exists():
            raise ValidationError('You have already reviewed this product.')
        data = request.data
        data['product'] = product_id
        data['user'] = user.id
        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get_object(self, pk, user):
        try:
            return Review.objects.get(pk=pk, user=user)
        except Review.DoesNotExist:
            raise NotFound('Review not found')

    def get(self, request, pk):
        review = self.get_object(pk, request.user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        review = self.get_object(pk, request.user)
        serializer = ReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        review = self.get_object(pk, request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
