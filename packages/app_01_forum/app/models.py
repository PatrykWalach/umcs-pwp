from __future__ import annotations

import re
import typing
from email.headerregistry import UniqueAddressHeader

import django.db.models as models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, F, Q
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import RowNumber
from django.urls import reverse
from django.utils.timezone import now, timedelta


class User(AbstractUser):
    avatar = models.URLField()

    def get_absolute_url(self) -> str:
        return reverse("user", kwargs={"slug": self.username})

    class Meta:
        db_table = "auth_user"


class SubTopic(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def new(self):
        return self.created_at > now() - timedelta(days=7)

    class Meta:
        unique_together = ["slug", "topic"]

    def __str__(self) -> str:
        return f"{str(self.topic) if self.topic != None else '/'}{self.slug}/"

    def path(self) -> list[SubTopic]:
        path = self.topic.path() if self.topic is not None else []

        return path + [self]

    def post_count(self):
        return self.thread_set.aggregate(Count("post"))["post__count"]

    def get_absolute_url(self) -> str:
        if self.topic == None:
            return reverse("topic", kwargs={"slug": self.slug})

        return reverse("topic", kwargs={"slug": self.slug, "topic_pk": self.topic.pk})


class Thread(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, default=None, blank=True)

    def is_closed(self) -> bool:
        return self.closed_at is not None and self.closed_at < now()

    def __str__(self) -> str:
        return f"{str(self.subtopic)}{self.pk}/"

    def get_absolute_url(self) -> str:
        return reverse("thread", kwargs={"pk": self.pk})


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    thread = models.ForeignKey(Thread, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "pk"
        ordering = ("pk",)

    def __str__(self) -> str:
        return str(self.pk)

    def get_absolute_url(self) -> str:
        posts: models.Manager[Post] = self.thread.post_set
        index = posts.filter(pk__lt=self.pk).count()

        page = index // 10 + 1

        return f"{self.thread.get_absolute_url()}?page={page}#post-{self.pk}"
