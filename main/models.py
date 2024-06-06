from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.models import UserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("name", "ahmed")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, null=True, unique=True)
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True, null=True)
    is_expert = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()


class Module(models.Model):
    name = models.CharField(max_length=255)
    tp_hours = models.FloatField()
    td_hours = models.FloatField()
    cours_hours = models.FloatField()

    def setModuleHours(self):
        pass


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    hours = models.FloatField()
    modules = models.ManyToManyField("Module", blank=True)

    def assignModule(self, module):
        self.modules.add(module)

class Classroom(models.Model):
    CLASSROM_TYPES = [("TD", "TD"), ("TP", "TP"), ("AMPHI", "AMPHI")]
    classroom_number = models.IntegerField()
    type = models.CharField(max_length=255, choices=CLASSROM_TYPES)

    def setAvailability(self):
        pass
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def assignModule(self, module):
        self.module = module
        self.save()

    def assignClassroom(self, classroom):
        self.classroom = classroom
        self.save()


class Group(models.Model):
    number = models.IntegerField()
    grade = models.IntegerField()
    semester = models.IntegerField()
    specialty = models.CharField(max_length=255)
    school_year = models.IntegerField()

    def setConstraints(self):
        pass


class Schedule(models.Model):
    time_slot = models.DurationField()
    time_slots = models.ManyToManyField(TimeSlot)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def assignGroup(self, group):
        self.group = group
        self.save()

    def addTimeSlot(self, time_slot):
        self.time_slots.add(time_slot)

    def validateSchedule(self):
        pass


