from __future__ import annotations

import re
import typing
from dataclasses import dataclass

import django.utils.timezone
from app.forms import CreatePostForm, CreateThreadForm
from app.models import Post, SubTopic, Thread
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Manager, Max, Model, OuterRef, Q, Subquery
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

T = typing.TypeVar("T", bound=Model)


class ThreadView(CreateView):
    template_name = "thread.html"
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = Thread.objects.get(slug=self.kwargs["thread"])
        return super().form_valid(form)

    def get_initial(self) -> typing.Dict[str, typing.Any]:
        return {
            "content": self.request.GET.get("content"),
        }

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**self.kwargs)

        thread = Thread.objects.get(slug=self.kwargs["thread"])
        posts: Manager[Post] = thread.post_set

        context["thread"] = thread

        paginator = Paginator(
            posts.all(),
            10,
        )
        page = self.request.GET.get("page", 1)
        context["paginator"] = paginator
        context["object_list"] = paginator.page(page)
        context["page"] = page

        context["preview"] = {
            "created_at": django.utils.timezone.now(),
            "content": self.request.GET.get("content"),
            "author": self.request.user,
        }

        return context


class UserView(DetailView):
    template_name = "user.html"
    slug_field = "username"
    slug_url_kwarg = "username"


class MainView(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:

        context = super().get_context_data(**kwargs)

        # recent_threads = (
        #     Thread.objects.filter(subtopic=OuterRef("pk"))
        #     .annotate(most_recent_post=Max("post__created_at"))
        #     .order_by("most_recent_post")
        # )

        context["subtopics"] = (
            SubTopic.objects.filter(topic__topic=None, topic__isnull=False)
            .annotate(post_count=Count("thread__post"))
            .order_by("topic")
        )

        return context


class TopicView(CreateView):
    template_name = "topic.html"
    form_class = CreateThreadForm

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
        context["topic"] = topic

        paginator = Paginator(
            threads.all(),
            10,
        )

        page = self.request.GET.get("page", 1)
        context["paginator"] = paginator
        context["object_list"] = paginator.page(page)
        context["page"] = page

        return context
