import uuid
from django.http import HttpRequest
from django.conf import settings
from django.urls import reverse
from yookassa import Payment, Configuration
from currency_converter import CurrencyConverter

from shop.models import NftProduct


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create(request: HttpRequest, nft: NftProduct) -> str:
    """
    Creates payment and returns tuple consists of
    redirect confirmation url and its uid
    """
    # conversion USD -> RUB on 01.03.2022
    c = CurrencyConverter()
    available_rub_range = c.bounds["RUB"]
    currently_price_in_rub = c.convert(
        nft.price, "USD",
        "RUB", available_rub_range[-1]
    )

    payment_uid = uuid.uuid4()

    payment = Payment.create({
        "amount": {
            "value": str(currently_price_in_rub),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(
                reverse("payment:completed",
                        args=[nft.id])
            )
        },
        "capture": True,
        "description": f"NFT {nft.name}"
    }, payment_uid)

    confirmation_url = payment.confirmation.confirmation_url
    request.session["payment_uid"] = payment.id
    print(payment.id)
    return confirmation_url


def check_status(request: HttpRequest) -> bool:
    """
    Checks payment status, if status is succeeded, it will return True
    if canceled, False
    """
    payment = Payment.find_one(request.session["payment_uid"])

    if payment.status == "succeeded":
        del request.session["payment_uid"]
        return True

    del request.session["payment_uid"]
    return False



