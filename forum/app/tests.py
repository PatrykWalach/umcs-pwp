from playwright.sync_api import Page, expect

from django.urls import reverse
import re
import os
import pytest
from django.contrib.auth.models import User
from app.models import Profile

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def test_main_page_title(live_server, page: Page):
    # when
    page.goto(live_server.url)
    # then
    expect(page).to_have_title("Forum")


def test_navbar_login_navigation(live_server, page: Page):
    # given
    page.goto(live_server.url)
    # when
    page.get_by_role("link", name="Login").click()
    # then
    expect(page).to_have_url(re.compile(reverse("login")))


def test_navbar_viewer_avatar(live_server, user: User, page: Page):
    # given
    profile = Profile.objects.create(avatar="http://www.test.com/avatar.png", user=user)
    # when
    page.goto(live_server.url)
    # then
    expect(page.get_by_role("navigation").get_by_role("img")).to_have_attribute(
        "src", profile.avatar
    )


def test_navbar_viewer_default_avatar(live_server, user: User, page: Page):
    # when
    page.goto(live_server.url)
    # then
    expect(page.get_by_role("navigation").get_by_role("img")).to_have_attribute(
        "src", "/static/avatar.gif"
    )


@pytest.fixture
def user(live_server, page: Page, django_user_model):
    user = django_user_model.objects.create_user(username="user", password="user")
    page.goto(live_server.url + reverse("login"))

    password = "user"
    page.get_by_role("textbox", name="Username:").type(user.username)
    page.get_by_role("textbox", name="Password:").type(password)
    page.get_by_role("button", name="Login").click()

    return user


def test_login(live_server, page: Page, django_user_model):
    # given
    page.goto(live_server.url + reverse("login"))

    password = "user"
    user = django_user_model.objects.create_user(username="user", password=password)

    page.get_by_role("textbox", name="Username:").type(user.username)
    page.get_by_role("textbox", name="Password:").type(password)
    # when
    page.get_by_role("button", name="Login").click()

    # then
    expect(page).to_have_title("Forum")


def test_duplicate_username(live_server, page: Page, django_user_model):
    # given
    page.goto(live_server.url + reverse("signup"))

    password = "user"
    user = django_user_model.objects.create_user(username="user", password=password)

    page.get_by_role("textbox", name="Password:").type(password)
    page.get_by_role("textbox", name="Password confirmation:").type(password)
    page.get_by_role("textbox", name="Username:").type(user.username)
    # when
    page.get_by_role("button", name="Register").click()
    # then
    page.get_by_text("A user with that username already exsists.")


from app.models import SubTopic, Thread, Post


def test_post_create(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        slug="user-thread",
        subtopic=SubTopic.objects.create(slug="general"),
    )
    page.goto(live_server.url + thread.get_absolute_url())
    page.get_by_placeholder("Reply to the topic...").type(
        "# Title\n\n - item 1\n - item 2"
    )
    # when
    page.get_by_role("button", name="Submit").click()
    # then
    page.get_by_role("heading", name="Title")
    page.get_by_role("listitem", name="item 1")
    page.get_by_role("listitem", name="item 2")
    assert Post.objects.get().content == "# Title\r\n\r\n - item 1\r\n - item 2"
    assert Post.objects.get().author == user
    assert Post.objects.get().thread == thread


def test_post_create_preview(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        slug="user-thread",
        subtopic=SubTopic.objects.create(slug="general"),
    )
    page.goto(live_server.url + thread.get_absolute_url())
    page.get_by_placeholder("Reply to the topic...").type(
        "# Title\n\n - item 1\n - item 2"
    )
    # when
    page.get_by_role("button", name="Preview").click()
    # then
    page.get_by_role("heading", name="Title")
    page.get_by_role("listitem", name="item 1")
    page.get_by_role("listitem", name="item 2")
    assert Post.objects.count() == 0
