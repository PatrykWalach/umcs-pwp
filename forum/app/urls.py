from __future__ import annotations

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
from dataclasses import dataclass
import re
import django.http
from django.contrib import admin
from django.shortcuts import render
from django.urls import path


from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

import django.contrib.auth.views
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import typing

from app.models import Post, SubTopic, Thread

import django.db.models

from app.views import MainView, ThreadView, TopicView, UserView

from django.db.models import Q, Count, Subquery, Max, OuterRef


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("profile.urls")),
    path("", MainView.as_view(), name="main"),
    path("user/<str:username>/", UserView.as_view(), name="user"),
    path("search/", TemplateView.as_view(template_name="search.html"), name="search"),
    path(
        "signup/",
        CreateView.as_view(
            form_class=UserCreationForm,
            template_name="signup.html",
            success_url=reverse_lazy("main"),
        ),
        name="signup",
    ),
    path("topic/<int:topic_pk>/<slug:topic>/", TopicView.as_view(), name="topic"),
    path("topic/<slug:topic>/", TopicView.as_view(), name="topic"),
    path(
        "thread/<int:topic_pk>/<slug:thread>/",
        ThreadView.as_view(),
        name="thread",
    ),
]
