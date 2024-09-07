from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html",
                  {"section": "dashboard"})
