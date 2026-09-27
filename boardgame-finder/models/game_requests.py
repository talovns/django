"""Заявки на поиск игроков: класс GameRequest и функции работы с заявками."""

from typing import Iterator, Optional

from .games import Game
from .meetings import Meeting
from .users import User


class GameRequest:
    """Заявка на поиск игроков: игра, автор, число мест и встреча."""

    def __init__(
        self,
        request_id: int,
        game: Game,
        author: User,
        players_needed: int,
        meeting: Meeting,
        players_joined: int = 0,
    ) -> None:
        """Создать заявку."""
        self.id = request_id
        self.game = game
        self.author = author
        self.players_needed = players_needed
        self.meeting = meeting
        self._players_joined = players_joined

    @property
    def players_joined(self) -> int:
        """Сколько игроков уже присоединилось."""
        return self._players_joined

    @property
    def is_open(self) -> bool:
        """Открыта ли заявка: есть ли свободные места."""
        return self.free_slots() > 0

    def free_slots(self) -> int:
        """Вычислить количество свободных мест (функция из ПР1)."""
        free_slots = self.players_needed - self._players_joined
        if free_slots < 0:
            return 0
        return free_slots

    def add_player(self) -> None:
        """Занять одно место в заявке."""
        if not self.is_open:
            raise ValueError("В заявке нет свободных мест")
        self._players_joined += 1

    def remove_player(self) -> None:
        """Освободить одно место в заявке."""
        if self._players_joined > 0:
            self._players_joined -= 1

    def __str__(self) -> str:
        """Вернуть описание заявки (бывшая format_meeting_info из ПР1)."""
        return (
            f"«{self.game.title}», встреча: {self.meeting}. "
            f"Автор: {self.author.name}. "
            f"Свободных мест: {self.free_slots()} из {self.players_needed}"
        )


def get_request_status(is_open: bool) -> str:
    """Вернуть текстовый статус заявки (функция из ПР1)."""
    if is_open:
        return "Заявка открыта, поиск игроков продолжается"
    return "Заявка закрыта"


def add_request(
    requests: list[GameRequest],
    game: Game,
    author: User,
    players_needed: int,
    meeting: Meeting,
) -> Optional[GameRequest]:
    """Создать заявку, если в игру можно играть таким числом игроков."""
    if not game.supports_players(players_needed):
        return None
    request_id = max((request.id for request in requests), default=0) + 1
    request = GameRequest(request_id, game, author, players_needed, meeting)
    requests.append(request)
    return request


def find_request(requests: list[GameRequest], query: str) -> list[GameRequest]:
    """Найти заявки по подстроке в названии игры или городе встречи."""
    query_lower = query.lower()
    return [
        request for request in requests
        if query_lower in request.game.title.lower()
        or query_lower in request.meeting.city.lower()
    ]


def find_request_by_id(requests: list[GameRequest], request_id: int) -> Optional[GameRequest]:
    """Найти заявку по идентификатору."""
    for request in requests:
        if request.id == request_id:
            return request
    return None


def filter_requests_by_free_slots(
    requests: list[GameRequest], min_free: int
) -> Iterator[GameRequest]:
    """Отобрать заявки со свободными местами не меньше min_free."""
    for request in requests:
        if request.free_slots() >= min_free:
            yield request


def sort_requests(requests: list[GameRequest]) -> list[GameRequest]:
    """Отсортировать заявки по свободным местам (по убыванию)."""
    return sorted(requests, key=lambda request: request.free_slots(), reverse=True)


def get_statistics(requests: list[GameRequest]) -> dict:
    """Вычислить статистику по заявкам: количество и свободные места."""
    total = len(requests)
    open_count = sum(1 for request in requests if request.is_open)
    return {
        "total": total,
        "open": open_count,
        "closed": total - open_count,
        "total_free_slots": sum(request.free_slots() for request in requests),
    }


def show_requests(requests: list[GameRequest]) -> None:
    """Вывести список заявок со статусом."""
    if not requests:
        print("Заявок нет")
        return
    for request in requests:
        print(f"[{request.id}] {request} — {get_request_status(request.is_open)}")
