from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html",
                  {"section": "dashboard"})


def registration(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data

            new_user = user_form.save(commit=False)
            new_user.set_password(cd["password"])
            new_user.save()

            return render(request, "account/register_done.html",
                          {"form": new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/registration.html",
                  {"form": user_form})
