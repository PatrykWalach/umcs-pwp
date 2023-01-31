from __future__ import annotations

import re
import typing
from dataclasses import dataclass

import django.utils.timezone
from app.forms import CreatePostForm, CreateThreadForm
from app.models import Post, SubTopic, Thread, User
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Manager, Max, Model, OuterRef, Q, Subquery
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now, timedelta
from django.views import View
from django.views.generic import CreateView, FormView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import UpdateView

T = typing.TypeVar("T", bound=Model)


@staff_member_required
def ThreadCloseView(request: HttpRequest, pk: int) -> HttpResponse:
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == "POST":
        thread.closed_at = now()
        thread.save()

    return redirect(thread.get_absolute_url())


def ThreadView(request: HttpRequest, pk: int) -> HttpResponse:
    thread = get_object_or_404(Thread, pk=pk)
    form = CreatePostForm(
        user=request.user, initial={"content": request.GET.get("content")}
    )

    if (
        request.method == "POST"
        and (form := CreatePostForm(request.POST)).is_valid()
        and not thread.is_closed()
    ):
        form.instance.author = request.user
        form.instance.thread = thread
        form.save()
        return redirect(form.instance.get_absolute_url())

    paginator = Paginator(
        thread.post_set.order_by("pk").all(),
        10,
    )

    page_obj = paginator.page(request.GET.get("page", 1))

    return render(
        request,
        "app/thread.html",
        {
            "object": thread,
            "paginator": paginator,
            "page_obj": page_obj,
            "object_list": page_obj.object_list,
            "form": form,
            "preview": {
                "created_at": django.utils.timezone.now(),
                "content": request.GET.get("content"),
                "author": request.user,
            },
        },
    )


class SettingsView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = User
    template_name = "app/settings.html"
    fields = ["username", "avatar"]

    def get_object(
        self, queryset: typing.Optional[QuerySet[typing.Any]] = ...
    ) -> Model:
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserView(SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = "app/user.html"
    slug_field = "username"
    context_object_name = "object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.post_set.all().order_by("-pk")


class MainView(ListView):
    template_name = "app/main.html"
    ordering = ("topic",)
    queryset = SubTopic.objects.filter(topic__topic=None, topic__isnull=False)


def UserDeleteView(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        request.user.is_active = False
        request.user.save()
        logout(request)
        return redirect("main")

    return redirect("settings")


def TopicView(
    request: HttpRequest, slug: str, topic_pk: int | None = None
) -> HttpResponse:
    subtopic = get_object_or_404(SubTopic, slug=slug, topic__pk=topic_pk)
    form = CreateThreadForm()

    if request.method == "POST" and (form := CreateThreadForm(request.POST)).is_valid():
        form.instance.author = request.user
        form.instance.subtopic = subtopic
        form.save()
        return redirect(form.instance.get_absolute_url())

    paginator = Paginator(
        subtopic.thread_set.order_by("-pk").all(),
        10,
    )

    page_obj = paginator.page(request.GET.get("page", 1))

    return render(
        request,
        "app/topic.html",
        {
            "object": subtopic,
            "paginator": paginator,
            "page_obj": page_obj,
            "object_list": page_obj.object_list,
            "form": form,
        },
    )
