from django.db import models

from shop.models import NftProduct


class Favorite(models.Model):
    profile = models.ForeignKey(to="account.Profile",
                                related_name="profile_favorites",
                                on_delete=models.CASCADE)
    nft = models.ForeignKey(to=NftProduct,
                            on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Profile {self.profile} -> NftProduct {self.nft}"
