"""Страницы заявок на поиск игроков."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models import GameRequest, Join
from models.game_requests import find_request_by_id, get_request_status
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
    items = ""
    for game_request in requests_list:
        status = "открыта" if game_request.is_open else "закрыта"
        badge = "bg-success" if game_request.is_open else "bg-secondary"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/requests/{game_request.id}/">
                {escape(game_request.game.title)} –
                {game_request.meeting.meeting_date.strftime('%d.%m.%Y')}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Заявки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Заявки – поиск игроков", content))


def request_detail(request: HttpRequest, request_id: int) -> HttpResponse:
    """Страница заявки: игра, автор, встреча, места и участники."""
    requests_list, joins_list = load_data()
    game_request = find_request_by_id(requests_list, request_id)
    if game_request is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/requests/" class="btn btn-outline-secondary">
            ← к списку заявок
        </a>
        """
        return HttpResponse(page("Заявка не найдена", content), status=404)

    players = "".join(
        f'<li class="list-group-item">{escape(join.user.name)}</li>'
        for join in joins_list
        if join.request is game_request and not join.is_cancelled
    )
    badge = "bg-success" if game_request.is_open else "bg-secondary"
    meeting = game_request.meeting
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заявка №{game_request.id}</h5>
            <p class="card-text">Игра: {escape(game_request.game.title)}</p>
            <p class="card-text">Автор: {escape(game_request.author.name)}</p>
            <p class="card-text">
                Встреча: {meeting.meeting_date.strftime('%d.%m.%Y')},
                {escape(meeting.city)}, {escape(meeting.place)}
            </p>
            <p class="card-text">
                Свободных мест: {game_request.free_slots()}
                из {game_request.players_needed}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">
                    {get_request_status(game_request.is_open)}
                </span>
            </p>
            <h6>Участники</h6>
            <ul class="list-group mb-3">{players}</ul>
            <a href="/requests/" class="btn btn-outline-secondary">
                ← к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заявка №{game_request.id}", content))
