from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    owner = models.OneToOneField(User,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to="account/%Y/%m/%d",
                              blank=True)
    date_of_birth = models.DateTimeField(null=True,
                                         blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile for {self.owner.username}"
