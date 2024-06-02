from rest_framework import generics
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer
from .models import User
from dj_rest_auth.views import LoginView

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        user = authenticate(
            email=self.request.data.get("email"),
            password=self.request.data.get("password"),
        )
        if user and user.is_active:
            login(self.request, user)