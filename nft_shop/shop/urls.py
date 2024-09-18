from django.urls import path

from . import views


app_name = "shop"

urlpatterns = [
    path("", views.nft_list, name="nft_list"),
    path("<slug:slug>/<int:nft_id>", views.NftDetail.as_view(), name="nft_detail")
]
