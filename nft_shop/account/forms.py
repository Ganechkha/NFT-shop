from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Profile


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput(attrs={'placeholder': 'repeat password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox,
                             public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY,
                             label="ReCAPTCHA")

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "first name"}),
            "email": forms.EmailInput(attrs={"placeholder": "E-mail"}),
        }

    def clean_password2(self) -> str:
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(r"Passwords didn`t match")
        return cd["password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name",
                  "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"placeholder": "your birth day"})
        }
