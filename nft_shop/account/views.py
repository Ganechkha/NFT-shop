from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import UserRegistrationForm, UserEditForm, \
    ProfileEditForm
from .tokens import account_activation_token
from .tasks import send_activation_email
from .models import Profile
from shop.models import NftProduct


User = get_user_model()


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    user_nfts = NftProduct.objects.filter(owner=request.user)

    profile_id = request.user.profile.id
    profile = Profile.objects.get(id=profile_id)
    user_favorites = profile.favorites.all()

    return render(request, "account/dashboard.html",
                  {"section": "dashboard",
                   "user_nfts": user_nfts,
                   "favorites": user_favorites})


def registration(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data

            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.set_password(cd["password"])
            new_user.save()

            send_activation_email.delay(new_user.id, new_user.email, request.get_host())

            return render(request, "account/register_done.html")
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/registration.html",
                  {"form": user_form})


def activate(request: HttpRequest, uidb64, token) -> HttpResponse:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # Creating profile for active user
        Profile.objects.get_or_create(owner=user)

        return render(request, "registration/activation_done.html")
    else:
        return render(request, "registration/activation_error.html")


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
                           "profile_form": profile_form,
                           "section": "dashboard"})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)

    return render(request, "account/profile_edit.html",
                  {"user_form": user_form,
                   "profile_form": profile_form,
                   "section": "dashboard"})
