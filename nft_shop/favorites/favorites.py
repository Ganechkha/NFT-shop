from typing import Generator

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest

from nft_shop.shop.models import NftProduct

User = get_user_model()


class Favorite:
    """
    Class describes a favorites for each user
    """
    def __init__(self, request: HttpRequest, user_id: int) -> None:
        self.user = User.objects.get(id=user_id)
        self.request = request
        self.session = request.session

        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not settings.FAVORITES_SESSION_ID:
            # favorites not defined
            favorites = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.favorites = favorites

    def favorites_add(self, nft_id: int) -> None:
        if nft := str(nft_id) in self.favorites:
            self.favorites[nft] = nft_id

    def favorites_remove(self, nft_id: int) -> None:
        if nft := str(nft_id) in self.favorites:
            self.favorites[nft] = nft_id

    def favorites_clear(self):
        self.favorites.clear()

    def __iter__(self) -> Generator[NftProduct]:
        """
        For each key in self.favorites extracts
        NftProduct object yields it
        """
        for value in self.favorites.values():
            nft = NftProduct.objects.get(id=value)

            yield nft
