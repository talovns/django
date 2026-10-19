"""Маршруты заявок на поиск игроков."""

from django.urls import path

from . import views

app_name = "gamerequests"

urlpatterns = [
    path("", views.game_requests, name="list"),
    path("<int:request_id>/", views.request_detail, name="detail"),
]
