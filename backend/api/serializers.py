# Import necessary modules from Django REST Framework
from rest_framework import serializers

# Import the User model from the 'api' app's models.py file
from api.models import User

# Define a serializer for the User model
# The serializer class inherits from ModelSerializer
# ModelSerializer is a class provided by Django REST Framework
# that allows you to easily create serializers for Django models
class UserSerializer(serializers.ModelSerializer):
    # Meta class is used to provide additional metadata to the serializer
    # Here, we specify the model to be used by the serializer
    # and the fields to be included in the serialized representation
    class Meta:
        model = User  # The model to be used by the serializer
        fields = '__all__'  # Include all fields of the model
        # extra_kwargs is a dictionary that allows you to set additional keyword arguments
        # for fields in the serializer
        # Here, we set the 'write_only' keyword argument for the 'password' field
        # to True, which means that the field will only be used when creating a new instance
        # and will not be included in the serialized representation of an existing instance
        extra_kwargs = {'password': {'write_only': True}}

    # The 'create' method is used to create a new instance of the model
    # based on the validated data
    # This method is automatically called when a POST request is made to the API endpoint
    # associated with the serializer
    def create(self, validated_data):
        # Retrieve the 'password' field from the validated data
        password = validated_data.pop('password', None)
        # Create a new instance of the model using the remaining validated data
        instance = self.Meta.model(**validated_data)
        # If a password was provided, set it using the 'set_password' method
        # This method is provided by the Django authentication system
        # and is used to securely set the password for a user
        if password is not None:
            instance.set_password(password)
        # Save the instance to the database
        instance.save()
        # Return the created instance
        return instance
