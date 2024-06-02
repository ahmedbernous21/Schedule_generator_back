from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import User
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name",)
