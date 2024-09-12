from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


app_name = "account"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("registration/", views.registration,
         name="registration"),
    path("edit/", views.profile_edit, name="profile_edit")
]
