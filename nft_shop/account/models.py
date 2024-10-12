from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from shop.models import NftProduct

User = get_user_model()


class Profile(models.Model):
    objects = models.Manager()

    owner = models.OneToOneField(to=User,
                                 blank=True,
                                 null=True,
                                 related_name="profile",
                                 on_delete=models.CASCADE)
    favorites = models.ManyToManyField(to=NftProduct,
                                       through="favorites.Favorite",
                                       related_name="users_added")

    image = models.ImageField(upload_to="account/%Y/%m/%d",
                              null=True,
                              blank=True)
    date_of_birth = models.DateField(null=True,
                                     blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile for {self.owner.username}"

    def get_absolute_url(self) -> str:
        return reverse("users:user_detail",
                       args=[self.id])
