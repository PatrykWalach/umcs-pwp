"""app1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import annotations

import typing

from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path


def app1_view(request: HttpRequest):
    return render(
        request,
        "template.html",
        {
            "items": list(request.GET.items()),
            "some": "URL search params:",
            "none": "No URL search params",
            "header": "App1",
        },
    )


def app2_view(request: HttpRequest, **kwargs: typing.Dict[str, str]):
    return render(
        request,
        "template.html",
        {
            "items": kwargs.items(),
            "some": "Params:",
            "none": "No params",
            "header": "App2",
        },
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("app1/", app1_view),
    path("app2/", app2_view),
    path("app2/<var1>/", app2_view),
    path("app2/<var1>/<var2>/", app2_view),
    path("app2/<var1>/<var2>/<var3>/", app2_view),
]
