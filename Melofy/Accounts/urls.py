from django.urls import path,include
from .views import ProfileRetrieve, ProfileRegister

urlpatterns = [
    path('<int:id>/', ProfileRetrieve.as_view(), name='Profile-Retrieve'),
    path('register/', ProfileRegister.as_view(), name='Profile-Register'),
]