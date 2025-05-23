from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Profile
from .serializers import ProfileRetrieveSerializers, ProfileRegisterSerializers, CustomAuthTokenSerializer



class ProfileRetrieve (generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ProfileRetrieveSerializers
    queryset = Profile.objects.filter(is_active=True)


class ProfileRegister(generics.GenericAPIView):
    serializer_class = ProfileRegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = ProfileRegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email'],
                'username': serializer.validated_data['username'],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


