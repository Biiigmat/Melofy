from django.urls import path,include
from .views import ProfileRetrieve, ProfileRegister, CustomAuthToken
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('<int:id>/', ProfileRetrieve.as_view(), name='Profile-retrieve'),
    path('register/', ProfileRegister.as_view(), name='Profile-register'),
    path('token/login/', CustomAuthToken.as_view(), name='Profile-token-login' ),
]