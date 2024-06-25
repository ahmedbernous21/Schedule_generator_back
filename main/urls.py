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
    GenerateScheduleView,
    GroupList,
    SlotDetail,
    SlotList,
)

urlpatterns = [
    path("api/users/", UserList.as_view(), name="users"),
    path("api/schedules/", ScheduleList.as_view(), name="schedules"),
    path("api/schedules/<int:pk>/", ScheduleDetail.as_view(), name="schedule-detail"),
    path("api/modules/", ModulesList.as_view(), name="modules"),
    path("api/slots/<int:pk>/", SlotDetail.as_view(), name="slot-detail"),
    path("api/slots/", SlotList.as_view(), name="slots"),
    path("api/modules/<int:pk>/", ModuleDetail.as_view(), name="module-detail"),
    path("api/teachers/", TeacherList.as_view(), name="teachers"),
    path("api/teachers/<int:pk>/", TeacherDetail.as_view(), name="teacher-detail"),
    path("api/plannings/", PlanningList.as_view(), name="plannings"),
    path("api/plannings/<int:pk>/", PlanningDetail.as_view(), name="planning-detail"),
    path("api/classrooms/", ClassroomList.as_view(), name="classrooms"),
    path(
        "api/classrooms/<int:pk>/", ClassroomDetail.as_view(), name="classroom-detail"
    ),
    path(
        "api/schedule/<int:planning_id>/",
        GenerateScheduleView.as_view(),
        name="generate-schedule",
    ),
    path("api/groups/", GroupList.as_view(), name="groups"),
]
