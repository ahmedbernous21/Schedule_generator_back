from django.urls import path
from .views import UserList


urlpatterns = [
	path('api/users/', UserList.as_view(), name="users"),
]