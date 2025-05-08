from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Profile
from .serializers import ProfileRetrieveSerializers, ProfileRegisterSerializers


class ProfileRetrieve (generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ProfileRetrieveSerializers
    queryset = Profile.objects.all()


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


