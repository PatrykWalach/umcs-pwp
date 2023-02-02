from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.flatpages.urls")),
    path("", TemplateView.as_view(template_name="app1.html")),
]
#
# FlatPage.objects.update_or_create(id=1,
#                                   defaults={'url': "/onas/", 'content': "<h1>onas</h1>", 'sites': 'localhost:8000'})
# # FlatPage.objects.update_or_create(id=2, url="kontakt/", content="kontakt")
# FlatPage.objects.update_or_create(id=3, url="regulamin/", content="regulamin")
