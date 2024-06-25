# views.py
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import (
    User,
    Schedule,
    TimeSlot,
    Module,
    Classroom,
    Teacher,
    Planning,
    Group,
)
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


class TeacherSerializer(serializers.ModelSerializer):
    planning = serializers.PrimaryKeyRelatedField(
        queryset=Planning.objects.all(), many=True
    )
    modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), many=True
    )

    class Meta:
        model = Teacher
        fields = "__all__"

    def create(self, validated_data):
        planning_data = validated_data.pop("planning", [])
        module_data = validated_data.pop("modules", [])

        teacher = Teacher.objects.create(**validated_data)

        # Add planning
        teacher.planning.set(planning_data)

        # Add modules
        teacher.modules.set(module_data)

        return teacher

    def update(self, instance, validated_data):
        planning_data = validated_data.pop(
            "planning", []
        )  # Ensure planning_data is not None
        instance.name = validated_data.get("name", instance.name)
        instance.hours = validated_data.get("hours", instance.hours)
        instance.save()
        instance.planning.set(planning_data)  # Update many-to-many relationships
        return instance


class ModuleSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Teacher.objects.all(), required=False
    )
    planning = serializers.PrimaryKeyRelatedField(
        queryset=Planning.objects.all(), many=True
    )

    class Meta:
        model = Module
        fields = "__all__"

    def create(self, validated_data):
        planning_data = validated_data.pop("planning")
        module = Module.objects.create(**validated_data)
        for planning_id in planning_data:
            module.planning.add(planning_id)
        return module


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = "__all__"

    def create(self, validated_data):
        planning_data = validated_data.pop("planning")
        classroom = Classroom.objects.create(**validated_data)
        for planning_id in planning_data:
            classroom.planning.add(planning_id)
        return classroom


class TimeSlotSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    classroom = ClassroomSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = "__all__"


class PlanningSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Planning
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = "__all__"


class ClassroomSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class TimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
