from celery import shared_task
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


@shared_task
def send_activation_email(user_id: int, to_email: str) -> None:
    user = User.objects.get(id=user_id)
    subject = "Activate your account"
    message = render_to_string("registration/activation_email.html", {
        "username": user.username,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[to_email]
    )
    email.send()
