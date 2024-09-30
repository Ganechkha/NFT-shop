from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"])
        ]


class SoldManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs) \
            .filter(is_sale=True)


class NftProduct(models.Model):
    objects = models.Manager()
    sold_objects = SoldManager()

    nft = models.ImageField(upload_to="shop/%Y/%m/%d")
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL)
    owner = models.ForeignKey(User,
                              related_name="nfts",
                              null=True,
                              on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=20,
                                decimal_places=2,
                                null=True,
                                blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_sale = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_sale"])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("shop:nft_detail",
                       args=[self.id,
                             self.slug])
