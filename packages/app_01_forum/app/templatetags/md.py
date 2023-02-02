from __future__ import annotations

from django import template
from django.template.defaultfilters import escape, stringfilter
from markdown import markdown

register = template.Library()


@register.filter
@stringfilter
def md(value):
    return markdown(
        escape(value),
        extensions=["markdown.extensions.tables", "markdown.extensions.fenced_code"],
    )
