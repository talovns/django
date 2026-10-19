"""Страницы каталога настольных игр."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.games import find_game_by_id
from storage import load_games, load_requests, load_users


def games(request: HttpRequest) -> HttpResponse:
    """Список игр каталога."""
    items = ""
    for game in load_games(str(settings.DATA_DIR / "games.json")):
        items += (
            f'<li class="list-group-item">'
            f'<a href="/games/{game.id}/">{escape(game.title)}</a> – '
            f"{game.min_players}-{game.max_players} игроков</li>"
        )
    content = f"""
    <h1>Игры</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Игры – поиск игроков", content))


def game_detail(request: HttpRequest, game_id: int) -> HttpResponse:
    """Страница игры: число игроков и открытые заявки на эту игру."""
    games_list = load_games(str(settings.DATA_DIR / "games.json"))
    game = find_game_by_id(games_list, game_id)
    if game is None:
        content = """
        <h1 class="text-danger">Игра не найдена</h1>
        <a href="/games/" class="btn btn-outline-secondary">← к списку игр</a>
        """
        return HttpResponse(page("Игра не найдена", content), status=404)

    users_list = load_users(str(settings.DATA_DIR / "users.json"))
    requests_list = load_requests(
        str(settings.DATA_DIR / "requests.json"), games_list, users_list
    )
    open_requests = [
        game_request for game_request in requests_list
        if game_request.game is game and game_request.is_open
    ]
    badge = "bg-success" if open_requests else "bg-secondary"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(game.title)}</h5>
            <p class="card-text"><strong>ID:</strong> {game.id}</p>
            <p class="card-text">
                <strong>Игроков:</strong> {game.min_players}-{game.max_players}
            </p>
            <p class="card-text">
                Открытых заявок:
                <span class="badge {badge}">{len(open_requests)}</span>
            </p>
            <a href="/games/" class="btn btn-outline-secondary">← к списку игр</a>
        </div>
    </div>
    """
    return HttpResponse(page(escape(game.title), content))
