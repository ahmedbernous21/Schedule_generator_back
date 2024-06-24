from rest_framework import generics
from django.contrib.auth import authenticate, login
from .serializers import (
    UserSerializer,
    ScheduleSerializer,
    ModuleSerializer,
    TeacherSerializer,
    PlanningSerializer,
    ClassroomSerializer,
)
from .models import User, Schedule, Module, Teacher, Planning, Classroom
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


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ModulesList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class PlanningList(generics.ListCreateAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer


class ClassroomList(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class ScheduleDetail(generics.RetrieveDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = "pk"


class ModuleDetail(generics.RetrieveDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "pk"


class TeacherDetail(generics.RetrieveDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = "pk"


class PlanningDetail(generics.RetrieveDestroyAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer
    lookup_field = "pk"


class ClassroomDetail(generics.RetrieveDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    lookup_field = "pk"
