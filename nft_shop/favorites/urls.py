from django.urls import path

from . import views


app_name = "favorites"

urlpatterns = [
    path("add/<int:nft_id>", views.favorites_add, name="add"),
    path("remove/<int:nft_id>", views.favorites_remove, name="remove"),
    path("clear/", views.favorites_clear, name="clear"),
]
