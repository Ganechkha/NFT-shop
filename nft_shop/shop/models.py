from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"])
        ]


class NftProduct(models.Model):
    objects = models.Manager()

    nft = models.ImageField(upload_to="shop/%Y/%m/%d")
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL)
    owner = models.OneToOneField(User,
                                 on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_sale = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_sale"])
        ]
