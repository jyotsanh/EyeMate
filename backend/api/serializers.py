from rest_framework import serializers
from api.models import User

# UserSerializer is a class that inherits from ModelSerializer.
# It is used to serialize and deserialize User instances.
class UserSerializer(serializers.ModelSerializer):
    """
    This class defines a serializer for the User model.

    The serializer is used to convert User instances to JSON data
    and vice versa.

    The Meta class is used to define the fields and extra kwargs
    for the serializer.

    The create and update methods are used to create and update
    User instances from validated data.

    The validate_email method is used to validate the email
    field of the User instance.

    This serializer is used by the API to create and update
    User instances.
    """
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True  # The password field is write-only
            },
            'email': {
                'required': True  # The email field is required
            },
            'is_admin': {
                'read_only': True  # The is_admin field is read-only
            }
        }

    def create(self, validated_data):
        """
        This method is used to create a User instance from validated data.

        :param validated_data: The validated data to create the User instance from
        :return: The created User instance
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        This method is used to update a User instance from validated data.

        :param instance: The User instance to update
        :param validated_data: The validated data to update the User instance from
        :return: The updated User instance
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_email(self, value):
        """
        This method is used to validate the email field of the User instance.

        :param value: The email value to validate
        :return: The validated email value
        """
        # Ensure email uniqueness
        if self.instance is None or self.instance.email != value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        return value

class AdminUserSerializer(UserSerializer):
    """
    This class defines a serializer for the User model that is used by the admin API.

    This serializer is similar to the UserSerializer, but it allows the
    is_admin field to be set.

    This serializer is used by the admin API to create and update
    User instances.
    """
    class Meta(UserSerializer.Meta):
        extra_kwargs = {
            'password': {
                'write_only': True  # The password field is write-only
            },
            'email': {
                'required': True  # The email field is required
            },
            'is_admin': {}  # Allow 'is_admin' to be set in admin serializer
        }

