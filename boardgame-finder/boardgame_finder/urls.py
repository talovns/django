"""Корневая маршрутизация: адреса распределяются между приложениями."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("games/", include("games.urls")),
    path("requests/", include("gamerequests.urls")),
]

handler404 = "homepage.views.page_not_found"
