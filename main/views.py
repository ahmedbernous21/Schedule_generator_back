from django.http import JsonResponse
from requests import Response
from rest_framework import generics
from django.contrib.auth import authenticate, login

from main.generator import ScheduleGenerator
from .serializers import (
    UserSerializer,
    ScheduleSerializer,
    ModuleSerializer,
    TeacherSerializer,
    PlanningSerializer,
    ClassroomSerializer,
    GroupSerializer,
    TimeSlotSerializer,
)
from .models import (
    User,
    Schedule,
    Module,
    Teacher,
    Planning,
    Classroom,
    Group,
    TimeSlot,
)
from dj_rest_auth.views import LoginView
from django.views import View
from rest_framework import viewsets, status


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


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = "pk"


class SlotList(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class SlotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    lookup_field = "pk"


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "pk"


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = "pk"


class PlanningDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer
    lookup_field = "pk"


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    lookup_field = "pk"


class GenerateScheduleView(View):
    def post(self, request, planning_id):
        generator = ScheduleGenerator(planning_id)
        message = generator.generate_schedule()
        return JsonResponse({"message": message})


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
