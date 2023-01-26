from __future__ import annotations

import app.forms as forms
import app.models as models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "topic", "created_at")


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "subtopic", "created_at")


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "avatar",
    )


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    form = forms.PostForm
    list_display = ("author", "thread", "content", "created_at")
