from django.urls import path

from . import views


app_name = "payment"

urlpatterns = [
    path("process/<int:nft_id>/", views.payment_process, name="process"),
    path("completed/<int:nft_id>/", views.payment_completed, name="completed")
]