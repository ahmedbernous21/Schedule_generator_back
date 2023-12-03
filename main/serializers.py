# views.py
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import User

class UserSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = User
        fields = ["name"]