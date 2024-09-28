from django import forms

from .models import NftProduct


class NftProductSellForm(forms.ModelForm):
    class Meta:
        model = NftProduct
        fields = ["description", "price"]

class UpdatePriceWithPercentsForm(forms.Form):
    PERCENT_CHOICES = [
        (0, "0%"),
        (10, "10%"),
        (20, "20%"),
        (30, "30%"),
        (40, "40%"),
        (50, "50%"),
        (100, "100%")
    ]

    price_increase = forms.ChoiceField(choices=PERCENT_CHOICES,
                                       label="Change percent to update your price",)
