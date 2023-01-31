from __future__ import annotations

import re
import typing
from dataclasses import dataclass

import django.contrib.auth.views
import django.db.models
import django.http
from app.forms import UserCreationForm
from app.models import Post, SubTopic, Thread
from app.views import (
    MainView,
    SettingsView,
    ThreadLockView,
    ThreadView,
    TopicView,
    UserRemoveView,
    UserView,
)
from django.contrib import admin
from django.db.models import Count, Max, OuterRef, Q, Subquery
from django.shortcuts import render
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

"""app URL Configuration

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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", MainView.as_view(), name="main"),
    path("user/<str:slug>/", UserView.as_view(), name="user"),
    path("user/", UserRemoveView, name="user-remove"),
    path(
        "search/", TemplateView.as_view(template_name="app/search.html"), name="search"
    ),
    path(
        "register/",
        CreateView.as_view(
            form_class=UserCreationForm,
            template_name="app/register.html",
            success_url=reverse_lazy("main"),
        ),
        name="register",
    ),
    path("topic/<int:topic_pk>/<slug:slug>/", TopicView, name="topic"),
    path("topic/<slug:slug>/", TopicView, name="topic"),
    path("settings", SettingsView.as_view(), name="settings"),
    path(
        "thread/<int:pk>/",
        ThreadView,
        name="thread",
    ),
    path(
        "thread/<int:pk>/lock/",
        ThreadLockView,
        name="thread-lock",
    ),
]
