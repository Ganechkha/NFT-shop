from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput(attrs={'placeholder': 'repeat password'}))

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
