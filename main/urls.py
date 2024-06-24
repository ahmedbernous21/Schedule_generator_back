from django.urls import path
from .views import (
    UserList,
    ScheduleList,
    ModulesList,
    TeacherList,
    PlanningList,
    ClassroomList,
    ScheduleDetail,
    ModuleDetail,
    TeacherDetail,
    PlanningDetail,
    ClassroomDetail,
)

urlpatterns = [
    path("api/users/", UserList.as_view(), name="users"),
    path("api/schedules/", ScheduleList.as_view(), name="schedules"),
    path("api/schedules/<int:pk>/", ScheduleDetail.as_view(), name="schedule-detail"),
    path("api/modules/", ModulesList.as_view(), name="modules"),
    path("api/modules/<int:pk>/", ModuleDetail.as_view(), name="module-detail"),
    path("api/teachers/", TeacherList.as_view(), name="teachers"),
    path("api/teachers/<int:pk>/", TeacherDetail.as_view(), name="teacher-detail"),
    path("api/plannings/", PlanningList.as_view(), name="plannings"),
    path("api/plannings/<int:pk>/", PlanningDetail.as_view(), name="planning-detail"),
    path("api/classrooms/", ClassroomList.as_view(), name="classrooms"),
    path(
        "api/classrooms/<int:pk>/", ClassroomDetail.as_view(), name="classroom-detail"
    ),
]
