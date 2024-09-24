from django.urls import path

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(),
         name="users_list"),
    path("<int:user_id>/<str:username>/",
         views.UserProfileDetail.as_view(),
         name="user_detail")
]