from django.http import JsonResponse, HttpRequest
from django.utils import timezone

from account.models import Profile
from shop.models import NftProduct


def favorites_add(request: HttpRequest, nft_id: int) -> JsonResponse:
    profile_id = request.user.profile.id
    profile = Profile.objects.get(id=profile_id)
    nft = NftProduct.sold_objects.get(id=nft_id)

    if nft in profile.favorites.all():
        return JsonResponse({
            "status": "not"
        })

    profile.favorites.add(nft, through_defaults={"added_at": timezone.now()})
    return JsonResponse({
        "status": "ok"
    })


def favorites_remove(request: HttpRequest, nft_id) -> JsonResponse:
    profile_id = request.user.profile.id
    profile = Profile.objects.get(id=profile_id)
    nft = NftProduct.sold_objects.get(id=nft_id)

    if nft not in profile.favorites.all():
        return JsonResponse({
            "status": "not"
        })

    profile.favorites.remove(nft)
    return JsonResponse({
        "status": "ok"
    })


def favorites_clear(request: HttpRequest) -> JsonResponse:
    pass