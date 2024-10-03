from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from shop.models import NftProduct
from .services import create, check_status



def payment_process(request: HttpRequest, nft_id: int):
    nft = NftProduct.sold_objects.get(id=nft_id)

    confirmation_url = create(request, nft)
    return redirect(confirmation_url)


def payment_completed(request: HttpRequest, nft_id: int) -> HttpResponse:
    nft = NftProduct.sold_objects.get(id=nft_id)

    if check_status(request):
        nft.owner = request.user
        nft.is_sale = False
        nft.save()

        return redirect("account:dashboard")

