from __future__ import annotations
import re
from django.db import IntegrityError


import typing
from dataclasses import dataclass
from django.views.generic.base import TemplateView
from app.forms import CreatePostForm, CreateThreadForm
from app.models import Post, SubTopic, Thread


@dataclass
class PageInfo:
    total_count: int
    page: int
    start_page: int = 0
    paginate = 5
    per_page = 10

    def end_page(self):
        return self.total_count // self.per_page

    def pages(self):
        return range(
            self.start_page + max(0, self.page - self.paginate - 1),
            self.start_page + min(self.page + self.paginate, self.end_page()),
        )

    def start_cursor(self):
        return (self.page - self.start_page) * self.per_page

    def end_cursor(self):
        return self.start_cursor() + self.per_page

    def slice(self):
        return slice(self.start_cursor(), self.end_cursor())


from django.db.models import Manager
from django.core.exceptions import ValidationError

from django.views.generic import CreateView


from django import forms

from django.urls import reverse_lazy


class ThreadView(CreateView):
    template_name = "thread.html"
    form_class = CreatePostForm

    def get_success_url(self):
        return reverse_lazy("thread", kwargs=self.kwargs)

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

        page_info = PageInfo(
            page=int(self.request.GET.get("page", 1)),
            total_count=posts.count(),
            start_page=1,
        )

        context["thread"] = thread
        context["page_info"] = page_info
        context["posts"] = posts.all()[page_info.slice()]
        context["preview"] = {
            "created_at": django.utils.timezone.now(),
            "content": self.request.GET.get("content"),
            "author": self.request.user,
        }

        return context


from django.contrib.auth.models import User


class UserView(TemplateView):
    template_name = "user.html"

    def get_context_data(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        context = super().get_context_data(**self.kwargs)
        context["user"] = User.objects.get(username=self.kwargs["username"])
        return context


import django.utils.timezone


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

        # print([*Post.objects.filter(subtopic__topic=None).distinct("subtopic")])

        return context


from django.db.models import Q, Count, Subquery, Max, OuterRef


class TopicView(CreateView):
    template_name = "topic.html"
    form_class = CreateThreadForm

    def get_success_url(self):
        object: Thread = self.object
        return reverse_lazy(
            "thread", kwargs={"thread": object.slug, "topic_pk": object.subtopic.pk}
        )

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

        page_info = PageInfo(
            page=int(self.request.GET.get("page", 1)),
            total_count=threads.count(),
            start_page=1,
        )
        context["threads"] = threads.all()[page_info.slice()]

        return context
