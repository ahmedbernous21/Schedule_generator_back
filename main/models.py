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
    TIME_CHOICES = [
        ("8h:00-9h:30", "8h:00-9h:30"),
        ("9h:30-11h:00", "9h:30-11h:00"),
        ("11h:00-12h:30", "11h:00-12h:30"),
        ("12h:30-14h:00", "12h:30-14h:00"),
        ("14h:00-15h:30", "14h:00-15h:30"),
        ("15h:30-17h:00", "15h:30-17h:00"),
    ]
    DAY_CHOICES = [
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
    ]
    TIMESLOT_TYPES = [("TD", "TD"), ("TP", "TP"), ("COURS", "COURS")]

    day = models.CharField(max_length=20, choices=DAY_CHOICES, default="")
    time = models.CharField(max_length=20, choices=TIME_CHOICES, default="")
    type = models.CharField(max_length=20, choices=TIMESLOT_TYPES, default="")
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

    def setConstraints(self):
        pass


class Schedule(models.Model):
    YEAR_CHOICES = [("2023/2024", "2023/2024"), ("2024/2025", "2024/2025")]
    time_slots = models.ManyToManyField(TimeSlot)
    grade = models.IntegerField(null=True)
    semester = models.IntegerField(null=True)
    school_year = models.CharField(max_length=20, choices=YEAR_CHOICES, default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules")

    def assignGroup(self, group):
        self.group = group
        self.save()

    def addTimeSlot(self, time_slot):
        self.time_slots.add(time_slot)

    def validateSchedule(self):
        pass


class Planning(models.Model):
    speciality = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    schedules = models.ForeignKey(Group, on_delete=models.CASCADE)
