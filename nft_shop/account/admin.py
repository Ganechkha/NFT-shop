from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "date_of_birth", "created", "updated"]
    raw_id_fields = ["owner"]
    ordering = ["-created"]
