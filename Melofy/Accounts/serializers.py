from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class ProfileRetrieveSerializers (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'image',]



class ProfileRegisterSerializers (serializers.ModelSerializer):
    Repeat_password = serializers.CharField(max_length=32)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'password', 'Repeat_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['Repeat_password']:
            raise serializers.ValidationError({'detail': 'Passwords are not match!'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'email': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('Repeat_password')
        return Profile.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
