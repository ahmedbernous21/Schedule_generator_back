from django.urls import path
from .views import UserList, ScheduleList


urlpatterns = [
    path("api/users/", UserList.as_view(), name="users"),
    path("api/schedules/", ScheduleList.as_view(), name="users"),
]
