from debug_toolbar.panels.sql.utils import ElideSelectListsFilter
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest


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

