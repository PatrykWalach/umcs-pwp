from __future__ import annotations

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.urls import include, path
from django.views.generic.base import TemplateView


class LoginRequired(LoginRequiredMixin, TemplateView):
    login_url = "/error_page/"
    redirect_field_name = None


urlpatterns = [
    path("main_page/", LoginRequired.as_view(template_name="profile/main.html")),
    path(
        "priva_page1/",
        LoginRequired.as_view(template_name="profile/priva1.html"),
        name="priva1",
    ),
    path(
        "priva_page2/",
        LoginRequired.as_view(template_name="profile/priva2.html"),
        name="priva2",
    ),
    path("error_page/", TemplateView.as_view(template_name="profile/error.html")),
]
