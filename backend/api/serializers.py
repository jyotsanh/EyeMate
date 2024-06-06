from rest_framework import serializers
from api.models import User

# UserSerializer is a class that inherits from ModelSerializer.
# It is used to serialize and deserialize User instances.
class UserSerializer(serializers.ModelSerializer):
    # Meta class provides configuration options for the UserSerializer.
    # It specifies the model that the UserSerializer is responsible for serializing and deserializing.
    # It also specifies the fields that should be included in the serialized representation of the User model.
    # The '__all__' value for the 'fields' attribute means that all fields of the User model are included.
    # The 'extra_kwargs' attribute is used to modify the serializer field settings.
    # The 'password' field is marked as 'write_only' which means that it is only used during deserialization (reading data from the API).
    # The 'email' field is marked as required, ensuring that the email field is always provided when creating or updating a user.
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}  # Ensure email is required
        }

    # The create method is used to create a new User instance from the validated data.
    # It takes the validated data as input and creates a new User instance.
    # The password is extracted from the validated data and set as the password of the User instance.
    # The User instance is saved to the database.
    # The created User instance is then returned.
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # The update method is used to update an existing User instance with the validated data.
    # It takes the existing User instance and the validated data as input.
    # The password is extracted from the validated data and set as the password of the User instance.
    # Each attribute of the User instance is updated with the corresponding value from the validated data.
    # The User instance is saved to the database.
    # The updated User instance is then returned.
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

