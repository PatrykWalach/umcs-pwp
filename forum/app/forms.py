import re
from django import forms
from app.models import (
    Post,
    Thread,
)
import django.db.models as models


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []
        widgets = {"content": forms.Textarea(attrs={"spellcheck": "true"})}


class Bubble(forms.Textarea):
    template_name = "django/forms/widgets/bubble.html"


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["author", "thread"]
        labels = {"content": ""}
        widgets = {
            "content": Bubble(
                attrs={"spellcheck": "true", "placeholder": "Reply to the topic..."}
            ),
        }


from django.core.exceptions import ValidationError


class SlugWidget(forms.TextInput):
    class Media:
        js = ("widget-slug.js",)


class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ["author", "subtopic"]
        # labels = {"content": ""}
        widgets = {
            # "author": forms.HiddenInput(),
            # "subtopic": forms.HiddenInput(),
            "slug": SlugWidget(),
            # "content": Bubble(
            #     attrs={"spellcheck": "true", "placeholder": "Replay to the topic..."}
            # )
        }
