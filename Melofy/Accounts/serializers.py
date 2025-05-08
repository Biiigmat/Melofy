from rest_framework import serializers
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class ProfileRetrieveSerializers (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'image']


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
