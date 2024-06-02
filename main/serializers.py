# views.py
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import User
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(UserSerializer, self).create(validated_data)
        return user


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={"input_type": "password"})
