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
from __future__ import annotations

import app.models as models
import django.http
from django.contrib import admin
from django.shortcuts import render
from django.urls import path


def lib_view(request: django.http.HttpRequest):
    i = int(request.POST.get("index", 0))
    query = models.Book.objects.all()

    return render(
        request,
        "lib_view.html",
        {
            "book": query[i],
            "next_index": i + 1,
            "prev_index": i - 1,
            "has_next": i + 1 < query.count(),
            "has_prev": i > 0,
        },
    )


def lib_add(request: django.http.HttpRequest):
    if request.method == "POST":
        book = models.Book(
            author=request.POST.get("author"),
            title=request.POST.get("title"),
            genre=request.POST.get("genre"),
        )
        book.save()

    return render(request, "lib_add.html")


def lib_main(request: django.http.HttpRequest):
    return render(
        request,
        "lib_main.html",
        {
            "book_count": models.Book.objects.all().count(),
            "books": models.Book.objects.all(),
        },
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("lib_main/", lib_main),
    path("lib_view/", lib_view),
    path("lib_add/", lib_add),
]
