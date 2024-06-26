from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


from rest_framework import serializers


class RegisterationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Must fill in all fields")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email has already been registered.')
        
        return attrs
    
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Create a new User instance with the provided data
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        return user
    

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["email"]


class EmailPasswordLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("must_include_email_and_password")
        

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise serializers.ValidationError("wrong_credentials")

        attrs['user'] = user
        return attrs