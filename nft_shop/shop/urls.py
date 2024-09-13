from django.urls import path

from . import views


app_name = "shop"

urlpatterns = [
    path("", views.NftListView.as_view(), name="nft_list")
]
