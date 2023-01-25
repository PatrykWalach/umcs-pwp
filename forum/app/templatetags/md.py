from django import template
from django.template.defaultfilters import stringfilter

from markdown import markdown

register = template.Library()


@register.filter
@stringfilter
def md(value):
    return markdown(
        value,
        extensions=["markdown.extensions.tables", "markdown.extensions.fenced_code"],
    )
