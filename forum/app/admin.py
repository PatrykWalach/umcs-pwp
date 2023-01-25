from django.contrib import admin
import app.models as models


@admin.register(models.SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "topic", "created_at")


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "slug", "author", "subtopic", "created_at")


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar")


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = "profile"


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


import app.forms as forms


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    form = forms.PostForm
    list_display = ("author", "thread", "content", "created_at")
