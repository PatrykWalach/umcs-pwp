from __future__ import annotations

import re
import typing
from dataclasses import dataclass

import django.utils.timezone
from app.forms import CreatePostForm, CreateThreadForm
from app.models import Post, SubTopic, Thread, User
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Manager, Max, Model, OuterRef, Q, Subquery
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import UpdateView

T = typing.TypeVar("T", bound=Model)


class ThreadView(CreateView):
    template_name = "app/thread.html"
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = Thread.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_initial(self) -> typing.Dict[str, typing.Any]:
        return {
            "content": self.request.GET.get("content"),
        }

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**self.kwargs)

        thread = Thread.objects.get(pk=self.kwargs["pk"])
        posts: Manager[Post] = thread.post_set

        context["object"] = thread

        paginator = Paginator(
            posts.order_by("pk").all(),
            10,
        )
        page = self.request.GET.get("page", 1)
        context["paginator"] = paginator
        page_obj = paginator.page(page)
        context["page_obj"] = page_obj
        context["object_list"] = page_obj.object_list
        context["page"] = page

        context["preview"] = {
            "created_at": django.utils.timezone.now(),
            "content": self.request.GET.get("content"),
            "author": self.request.user,
        }

        return context


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
        return self.object.post_set.all()


class MainView(ListView):
    template_name = "app/main.html"
    ordering = ("topic",)
    queryset = SubTopic.objects.filter(topic__topic=None, topic__isnull=False)


class TopicView(CreateView):
    template_name = "app/topic.html"
    form_class = CreateThreadForm
    # model = Thread
    # fields = ["title"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.subtopic = SubTopic.objects.get(
            slug=self.kwargs["topic"], topic__pk=self.kwargs.get("topic_pk", None)
        )
        return super().form_valid(form)

    def get_initial(self) -> typing.Dict[str, typing.Any]:
        return {
            "slug": self.request.GET.get("slug"),
        }

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)

        topic = SubTopic.objects.get(
            slug=self.kwargs["topic"], topic__pk=self.kwargs.get("topic_pk", None)
        )
        threads: Manager[Thread] = topic.thread_set
        context["object"] = topic

        paginator = Paginator(
            threads.order_by("-pk").all(),
            10,
        )

        page = self.request.GET.get("page", 1)
        page_obj = paginator.page(page)

        context["paginator"] = paginator
        context["page_obj"] = page_obj
        context["object_list"] = page_obj.object_list
        context["page"] = page

        return context
