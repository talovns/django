"""Главная страница и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание сервиса и ссылки на разделы."""
    return render(request, "homepage/index.html")


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница 404 (работает при DEBUG = False)."""
    return render(request, "homepage/404.html", status=404)
