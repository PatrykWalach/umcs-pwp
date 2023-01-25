from __future__ import annotations
from email.headerregistry import UniqueAddressHeader
import re
import typing
from django.utils.timezone import timedelta, now
import django.db.models as models
from django.contrib.auth.models import User


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


from django.db.models.constraints import UniqueConstraint


class Thread(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["slug", "subtopic"]
        # constraints = [UniqueConstraint(fields=["slug", "subtopic"], name='unique_slug')]

    def __str__(self) -> str:
        return f"{str(self.subtopic)}{self.slug}/"

    def post_count(self):
        return self.post_set.count()

    def validate_unique(
        self, exclude: typing.Optional[typing.Collection[str]] = ...
    ) -> None:
        return super().validate_unique()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    thread = models.ForeignKey(Thread, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        pass

    def __str__(self) -> str:
        return str(self.pk)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField()

    def __str__(self) -> str:
        return self.user.username
