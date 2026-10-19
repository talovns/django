"""Страницы каталога настольных игр."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.games import find_game_by_id
from storage import load_games, load_requests, load_users


def games(request: HttpRequest) -> HttpResponse:
    """Список игр каталога."""
    context = {
        "games": load_games(str(settings.DATA_DIR / "games.json")),
    }
    return render(request, "games/game_list.html", context)


def game_detail(request: HttpRequest, game_id: int) -> HttpResponse:
    """Страница игры: число игроков и открытые заявки на эту игру."""
    games_list = load_games(str(settings.DATA_DIR / "games.json"))
    game = find_game_by_id(games_list, game_id)
    open_requests = []
    if game is not None:
        users_list = load_users(str(settings.DATA_DIR / "users.json"))
        requests_list = load_requests(
            str(settings.DATA_DIR / "requests.json"), games_list, users_list
        )
        open_requests = [
            game_request for game_request in requests_list
            if game_request.game is game and game_request.is_open
        ]
    context = {
        "game": game,
        "open_requests": open_requests,
    }
    return render(
        request,
        "games/game_detail.html",
        context,
        status=404 if game is None else 200,
    )
