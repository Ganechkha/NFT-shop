from django.urls import path

from . import views


app_name = "users"


urlpatterns = [
    path("", views.UserListView.as_view(),
         name="users_list"),
    path("user/<int:pk>/",
         views.UserProfileDetail.as_view(),
         name="user_detail"),
]