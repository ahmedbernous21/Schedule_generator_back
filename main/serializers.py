# views.py
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import User, Schedule, TimeSlot, Module, Classroom
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


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = "__all__"


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = "__all__"


class TimeSlotSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = "__all__"
