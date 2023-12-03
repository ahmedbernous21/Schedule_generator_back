from rest_framework import generics
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer
from .models import User

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer