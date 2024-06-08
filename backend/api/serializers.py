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


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields=['email', 'username','first_name', 'last_name', 'password', 'password2']
        extra_kwargs={
        'password':{'write_only':True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        email = attrs.get('email')
        username = attrs.get('username')
        if User.objects.filter(email=email).exists(): # checks if the user with this email already exists
            raise serializers.ValidationError("User with this email already exists")

        if User.objects.filter(username=username).exists(): # checks if the user with this username already exists
            raise serializers.ValidationError("User with this username already exists")
        return attrs
    # Override create method to handle 'password2' validation
    def create(self, validated_data):
        # Pop 'password2' from validated_data
        password2 = validated_data.pop('password2')
        # Call the superclass's create method to create the user
        user = super().create(validated_data)
        # Set the password for the user
        user.set_password(validated_data['password'])
        # Save the user
        user.save()
        return user
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']