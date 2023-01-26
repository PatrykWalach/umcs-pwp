from __future__ import annotations

import re
import typing
from email.headerregistry import UniqueAddressHeader

import django.db.models as models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import RowNumber
from django.urls import reverse
from django.utils.timezone import now, timedelta


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

    def get_absolute_url(self):
        if self.topic == None:
            return reverse("topic", kwargs={"topic": self.slug})

        return reverse("topic", kwargs={"topic": self.slug, "topic_pk": self.topic.pk})


class Thread(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["slug", "subtopic"]

    def __str__(self) -> str:
        return f"{str(self.subtopic)}{self.slug}/"

    def post_count(self):
        return self.post_set.count()

    def validate_unique(
        self, exclude: typing.Optional[typing.Collection[str]] = ...
    ) -> None:
        return super().validate_unique()

    def get_absolute_url(self):
        return reverse(
            "thread", kwargs={"thread": self.slug, "topic_pk": self.subtopic.pk}
        )


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    thread = models.ForeignKey(Thread, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "pk"

    def __str__(self) -> str:
        return str(self.pk)

    def get_absolute_url(self):
        posts: models.Manager[Post] = self.thread.post_set
        index = posts.filter(pk__lt=self.pk).count()

        page = index // 10 + 1

        return f"{self.thread.get_absolute_url()}?page={page}#post-{self.pk}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField()

    def __str__(self) -> str:
        return self.user.username
