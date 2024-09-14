from django.contrib import admin

from .models import Category, NftProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(NftProduct)
class NftProductAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]
    search_fields = ["name", "owner"]
    raw_id_fields = ["owner"]
