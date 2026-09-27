"""Сохранение и загрузка данных: JSON <-> объекты предметной области."""

import json
from pathlib import Path

from models import Game, GameRequest, Join, Meeting, User
from models.game_requests import find_request_by_id
from models.games import find_game_by_id
from models.users import find_user_by_id


def read_json(filename: str) -> list[dict]:
    """Прочитать список записей из JSON-файла; при ошибке вернуть пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json(filename: str, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_games(filename: str) -> list[Game]:
    """Загрузить каталог игр."""
    return [Game.from_data(item) for item in read_json(filename)]


def load_users(filename: str) -> list[User]:
    """Загрузить игроков."""
    return [User.from_data(item) for item in read_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить игроков."""
    write_json(filename, [
        {"id": user.id, "name": user.name, "city": user.city} for user in users
    ])


def load_requests(filename: str, games: list[Game], users: list[User]) -> list[GameRequest]:
    """Загрузить заявки и связать их с объектами Game и User."""
    requests = []
    for item in read_json(filename):
        game = find_game_by_id(games, item["game_id"])
        author = find_user_by_id(users, item["author_id"])
        if game is None or author is None:
            continue
        requests.append(GameRequest(
            item["id"],
            game,
            author,
            item["players_needed"],
            Meeting.from_data(item["meeting"]),
            item["players_joined"],
        ))
    return requests


def save_requests(filename: str, requests: list[GameRequest]) -> None:
    """Сохранить заявки: вместо объектов записываются их идентификаторы."""
    write_json(filename, [
        {
            "id": request.id,
            "game_id": request.game.id,
            "author_id": request.author.id,
            "players_needed": request.players_needed,
            "players_joined": request.players_joined,
            "meeting": {
                "date": request.meeting.meeting_date.isoformat(),
                "city": request.meeting.city,
                "place": request.meeting.place,
            },
        }
        for request in requests
    ])


def load_joins(filename: str, requests: list[GameRequest], users: list[User]) -> list[Join]:
    """Загрузить участия и связать их с объектами GameRequest и User."""
    joins = []
    for item in read_json(filename):
        request = find_request_by_id(requests, item["request_id"])
        user = find_user_by_id(users, item["user_id"])
        if request is None or user is None:
            continue
        joins.append(Join(item["id"], request, user, item["is_cancelled"]))
    return joins


def save_joins(filename: str, joins: list[Join]) -> None:
    """Сохранить участия: вместо объектов записываются их идентификаторы."""
    write_json(filename, [
        {
            "id": join.id,
            "request_id": join.request.id,
            "user_id": join.user.id,
            "is_cancelled": join.is_cancelled,
        }
        for join in joins
    ])
