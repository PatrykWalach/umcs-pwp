from __future__ import annotations

import re

import django.db.models as models
from app.models import Post, Thread, User
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []
        widgets = {"content": forms.Textarea(attrs={"spellcheck": "true"})}


class Bubble(forms.Textarea):
    template_name = "django/forms/widgets/bubble.html"

    def get_context(self, *args, **kwargs) -> Dict[str, Any]:
        return super().get_context(*args, **kwargs) | {"user": self.user}


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["author", "thread"]
        labels = {"content": ""}
        help_texts = {"content": "You can use markdown"}
        widgets = {
            "content": Bubble(
                attrs={"spellcheck": "true", "placeholder": "Reply to the topic..."}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.user = user


class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ["author", "subtopic"]
        # labels = {"content": ""}
        widgets = {
            # "author": forms.HiddenInput(),
            # "subtopic": forms.HiddenInput(),
            # "content": Bubble(
            #     attrs={"spellcheck": "true", "placeholder": "Replay to the topic..."}
            # )
        }


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
