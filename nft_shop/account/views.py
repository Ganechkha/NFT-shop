from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm, UserEditForm, \
    ProfileEditForm


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


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return render(request, "account/profile_edit.html",
                          {"user_form": user_form,
                           "profile_form": profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)

    return render(request, "account/profile_edit.html",
                  {"user_form": user_form,
                   "profile_form": profile_form})
