from __future__ import annotations

import os
import re

import pytest
from app.models import Post, SubTopic, Thread, User
from django.urls import reverse
from django.utils.text import slugify
from playwright.sync_api import Page, expect

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@pytest.fixture(autouse=True)
def set_default_navigation_timeout(page: Page):
    page.set_default_navigation_timeout(3000)


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
    avatar = "https://media.giphy.com/media/a6pzK009rlCak/giphy.gif"
    user.avatar = avatar
    user.save()
    # when
    page.goto(live_server.url)
    # then
    expect(page.get_by_role("navigation").get_by_role("img")).to_have_attribute(
        "src", avatar
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
    password = "user"
    user = django_user_model.objects.create_user(username="user", password=password)
    page.goto(live_server.url + reverse("login"))

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
    page.goto(live_server.url + reverse("register"))

    password = "user"
    user = django_user_model.objects.create_user(username="user", password=password)

    page.get_by_role("textbox", name="Password:").type(password)
    page.get_by_role("textbox", name="Password confirmation:").type(password)
    page.get_by_role("textbox", name="Username:").type(user.username)
    # when
    page.get_by_role("button", name="Register").click()
    # then
    expect(page.get_by_text("A user with that username already exists.")).to_have_count(
        1
    )


def test_thread_create(live_server, page: Page, user):
    # given
    topic = SubTopic.objects.create(slug="general")
    page.goto(live_server.url + topic.get_absolute_url())
    title = "Title"
    page.get_by_label("Title:").type(title)
    # when
    page.get_by_role("button", name="create thread").click()
    # then
    assert Thread.objects.get().subtopic == topic
    assert Thread.objects.get().author == user
    assert Thread.objects.get().title == title


def test_post_create(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        subtopic=SubTopic.objects.create(slug="general"),
    )
    page.goto(live_server.url + thread.get_absolute_url())
    page.get_by_placeholder("Reply to the topic...").type(
        "# Title\n\n - item 1\n - item 2"
    )
    # when
    page.get_by_role("button", name="Submit").click()
    # then
    expect(page.get_by_role("heading", name="Title")).to_have_count(1)
    # expect(page.get_by_role("listitem", name="item 1")).to_have_count(1)
    # expect(page.get_by_role("listitem", name="item 2")).to_have_count(1)
    assert Post.objects.get().content == "# Title\r\n\r\n - item 1\r\n - item 2"
    assert Post.objects.get().author == user
    assert Post.objects.get().thread == thread


def test_post_create_preview(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        subtopic=SubTopic.objects.create(slug="general"),
    )
    page.goto(live_server.url + thread.get_absolute_url())
    page.get_by_placeholder("Reply to the topic...").type(
        "# Title\n\n - item 1\n - item 2"
    )
    # when
    page.get_by_role("button", name="Preview").click()
    # then
    expect(page.get_by_role("heading", name="Title")).to_have_count(1)
    # expect(page.get_by_role("listitem", name="item 1")).to_have_count(1)
    # expect(page.get_by_role("listitem", name="item 2")).to_have_count(1)
    assert Post.objects.count() == 0


def test_post_create_anonymous(live_server, page: Page, django_user_model):
    # given
    thread = Thread.objects.create(
        author=django_user_model.objects.create_user(username="user"),
        subtopic=SubTopic.objects.create(slug="general"),
    )
    # when
    page.goto(live_server.url + thread.get_absolute_url())
    # then
    expect(
        page.get_by_text("You need to be a member in order to leave a comment")
    ).to_have_count(1)


def test_thread_create_anonymous(live_server, page: Page, django_user_model):
    # given
    topic = SubTopic.objects.create(slug="general")
    # when
    page.goto(live_server.url + topic.get_absolute_url())
    # then
    expect(
        page.get_by_text("You need to be a member in order to create a new thread")
    ).to_have_count(1)


def test_post_pagination_navigation(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        subtopic=SubTopic.objects.create(slug="general"),
    )
    Post.objects.bulk_create(
        Post(thread=thread, author=user, content="# Test") for _ in range(100)
    )
    page.goto(live_server.url + thread.get_absolute_url())
    # when
    page.get_by_role("link", name="Go to page 2").first.click()
    # then
    expect(page).to_have_url(live_server.url + thread.get_absolute_url() + "?page=2")


def test_post_pagination_initial(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        subtopic=SubTopic.objects.create(slug="general"),
    )
    Post.objects.bulk_create(
        Post(thread=thread, author=user, content="# Test") for _ in range(100)
    )
    # when
    page.goto(live_server.url + thread.get_absolute_url())
    # then
    expect(page.get_by_role("heading", name="Test")).to_have_count(10)
    expect(page.get_by_role("link", name="Go to first page")).to_have_count(0)
    expect(page.get_by_role("link", name="Go to page -1")).to_have_count(0)
    expect(page.get_by_role("link", name="Go to page 0")).to_have_count(0)
    for i in range(1, 7):
        expect(page.get_by_role("link", name=f"Go to page {i}")).to_have_count(2)
    expect(page.get_by_role("link", name="Go to page 7")).to_have_count(0)
    expect(page.get_by_role("link", name="Go to last page")).to_have_count(2)


def test_post_pagination(live_server, page: Page, user: User):
    # given
    thread = Thread.objects.create(
        author=user,
        subtopic=SubTopic.objects.create(slug="general"),
    )
    Post.objects.bulk_create(
        Post(thread=thread, author=user, content="# Test") for _ in range(100)
    )
    # when
    page.goto(live_server.url + thread.get_absolute_url() + "?page=7")
    # then
    expect(page.get_by_role("heading", name="Test")).to_have_count(10)
    expect(page.get_by_role("link", name="Go to first page")).to_have_count(2)
    for i in range(-1, 2):
        expect(
            page.get_by_role("link", exact=True, name=f"Go to page {i}")
        ).to_have_count(0)
    for i in range(2, 11):
        expect(page.get_by_role("link", name=f"Go to page {i}")).to_have_count(2)
    expect(page.get_by_role("link", name="Go to page 11")).to_have_count(0)
    expect(page.get_by_role("link", name="Go to page 12")).to_have_count(0)
    expect(page.get_by_role("link", name="Go to last page")).to_have_count(2)
