from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import (
    User,
    Module,
    Teacher,
    Classroom,
    TimeSlot,
    Group,
    Schedule,
    Planning,
)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "tp_hours", "td_hours", "cours_hours")
    search_fields = ("name",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "hours")
    search_fields = ("name",)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("classroom_number", "type")
    search_fields = ("classroom_number", "type")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("time", "day", "type", "module", "classroom")
    search_fields = ("day", "module__name", "classroom__classroom_number")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("number",)
    search_fields = ("number", "specialty")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "group")
    search_fields = ("group__number", "group__specialty")


@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = ("id", "speciality", "grade", "semester", "school_year")
    search_fields = ("group__number", "group__specialty")
