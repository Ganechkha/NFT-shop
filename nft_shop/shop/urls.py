from django.urls import path

from . import views


app_name = "shop"

urlpatterns = [
    path("", views.nft_list, name="nft_list"),
    path("sell/<int:nft_id>", views.put_nft_on_sale,
         name="put_nft_on_sale"),
    path("sell/update_price/<int:nft_id>", views.nft_price_update,
         name="update_price"),
    path("<slug:category_slug>", views.nft_list,
         name="nft_list_by_category"),
    path("<slug:slug>/<int:nft_id>", views.NftDetail.as_view(),
         name="nft_detail"),
]
