from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, include


from django.contrib.auth.mixins import AccessMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

import logging


class LoginRequired(LoginRequiredMixin, TemplateView):
    login_url = "/error_page/"
    redirect_field_name = None

    def handle_no_permission(self) -> HttpResponseRedirect:
        logging.getLogger("LoginRequired.handle_no_permission").error(
            'No permission to "'
            + str(self.request.method)
            + " "
            + self.request.path
            + ""
            + '", redirecting to "'
            + self.login_url
            + '"'
        )
        return super().handle_no_permission()


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
