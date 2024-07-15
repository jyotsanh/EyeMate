from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Review, Product
from api.serializers import ReviewSerializer
from rest_framework.exceptions import NotFound, ValidationError
from api.renderers import CustomJSONRenderer

# ReviewListView is an APIView that handles GET and POST requests to the /api/reviews/<product_id> endpoint.
class ReviewListView(APIView):
    # Set the permission class to IsAuthenticated, which means only authenticated users can access this view.
    permission_classes = [IsAuthenticated]
    # Set the renderer class to CustomJSONRenderer, which means the response will be serialized in JSON format.
    renderer_classes = [CustomJSONRenderer]

    # GET request handler. Returns a list of all reviews for a given product.
    def get(self, request, product_id):
        # Retrieve all reviews for the product with the specified product_id.
        reviews = Review.objects.filter(product_id=product_id)
        # Serialize the reviews into JSON format.
        serializer = ReviewSerializer(reviews, many=True)
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST request handler. Creates a new review for a product.
    def post(self, request, product_id):
        # Retrieve the authenticated user.
        user = request.user
        # Retrieve the product with the specified product_id.
        product = Product.objects.get(id=product_id)
        # Check if the user has already reviewed the product.
        if Review.objects.filter(product=product, user=user).exists():
            # If the user has already reviewed the product, raise a ValidationError.
            raise ValidationError('You have already reviewed this product.')
        # Retrieve the review data from the request.
        data = request.data
        # Add the product_id and user_id to the review data.
        data['product'] = product_id
        data['user'] = user.id
        # Serialize the review data into JSON format.
        serializer = ReviewSerializer(data=data)
        # Validate the serialized data. If it's not valid, raise an exception.
        serializer.is_valid(raise_exception=True)
        # Save the validated data to the database.
        serializer.save()
        # Return the serialized data as the response with a 201 Created status code.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ReviewDetailView is an APIView that handles GET, PUT, and DELETE requests to the /api/reviews/<pk> endpoint.
class ReviewDetailView(APIView):
    # Set the permission class to IsAuthenticated, which means only authenticated users can access this view.
    permission_classes = [IsAuthenticated]
    # Set the renderer class to CustomJSONRenderer, which means the response will be serialized in JSON format.
    renderer_classes = [CustomJSONRenderer]

    # Helper method to retrieve a review object by primary key and user.
    def get_object(self, pk, user):
        try:
            return Review.objects.get(pk=pk, user=user)
        except Review.DoesNotExist:
            raise NotFound('Review not found')

    # GET request handler. Returns a single review by primary key and user.
    def get(self, request, pk):
        # Retrieve the review object by primary key and user.
        review = self.get_object(pk, request.user)
        # Serialize the review object into JSON format.
        serializer = ReviewSerializer(review)
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT request handler. Updates a review object by primary key and user.
    def put(self, request, pk):
        # Retrieve the review object by primary key and user.
        review = self.get_object(pk, request.user)
        # Serialize the review object into JSON format with the updated data from the request.
        serializer = ReviewSerializer(review, data=request.data)
        # Validate the serialized data. If it's not valid, raise an exception.
        serializer.is_valid(raise_exception=True)
        # Save the validated data to the database.
        serializer.save()
        # Return the serialized data as the response with a 200 OK status code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE request handler. Deletes a review object by primary key and user.
    def delete(self, request, pk):
        # Retrieve the review object by primary key and user.
        review = self.get_object(pk, request.user)
        # Delete the review object from the database.
        review.delete()
        # Return a blank response with a 204 No Content status code.
        return Response(status=status.HTTP_204_NO_CONTENT)

