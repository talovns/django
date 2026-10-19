"""Страницы заявок на поиск игроков."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import GameRequest, Join
from models.game_requests import find_request_by_id
from storage import load_games, load_joins, load_requests, load_users


def load_data() -> tuple[list[GameRequest], list[Join]]:
    """Загрузить заявки и участия со связями на игры и игроков."""
    games_list = load_games(str(settings.DATA_DIR / "games.json"))
    users_list = load_users(str(settings.DATA_DIR / "users.json"))
    requests_list = load_requests(
        str(settings.DATA_DIR / "requests.json"), games_list, users_list
    )
    joins_list = load_joins(
        str(settings.DATA_DIR / "joins.json"), requests_list, users_list
    )
    return requests_list, joins_list


def game_requests(request: HttpRequest) -> HttpResponse:
    """Список заявок со статусом открыта/закрыта."""
    requests_list, _ = load_data()
    context = {
        "game_requests": requests_list,
    }
    return render(request, "gamerequests/request_list.html", context)


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    """Страница заявки: игра, автор, встреча, места и участники."""
    requests_list, joins_list = load_data()
    game_request = find_request_by_id(requests_list, request_id)
    players = [
        join.user for join in joins_list
        if join.request is game_request and not join.is_cancelled
    ]
    context = {
        "game_request": game_request,
        "players": players,
    }
    return render(
        request,
        "gamerequests/request_detail.html",
        context,
        status=404 if game_request is None else 200,
    )
