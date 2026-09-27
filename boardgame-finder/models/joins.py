"""Участие игроков в заявках: класс Join и функции работы с участиями."""

from typing import Optional

from .game_requests import GameRequest
from .users import User


class Join:
    """Участие игрока в заявке."""

    def __init__(
        self, join_id: int, request: GameRequest, user: User, is_cancelled: bool = False
    ) -> None:
        """Создать участие игрока в заявке."""
        self.id = join_id
        self.request = request
        self.user = user
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить участие и освободить место в заявке."""
        if self.is_cancelled:
            return
        self.is_cancelled = True
        self.request.remove_player()

    def __str__(self) -> str:
        """Вернуть описание участия с его состоянием."""
        status = "отменено" if self.is_cancelled else "активно"
        return (
            f"{self.user.name} -> «{self.request.game.title}» "
            f"(заявка {self.request.id}, {status})"
        )


def can_join_request(joins: list[Join], request: GameRequest, user: User) -> bool:
    """Проверить, может ли игрок присоединиться к заявке."""
    if not request.is_open:
        return False
    for join in joins:
        if join.request is request and join.user is user and not join.is_cancelled:
            return False
    return True


def create_join(joins: list[Join], request: GameRequest, user: User) -> Optional[Join]:
    """Записать игрока в заявку; вернуть None, если это невозможно."""
    if not can_join_request(joins, request, user):
        return None
    join_id = max((join.id for join in joins), default=0) + 1
    join = Join(join_id, request, user)
    request.add_player()
    joins.append(join)
    return join


def cancel_join(joins: list[Join], join_id: int) -> bool:
    """Найти активное участие и отменить его."""
    for join in joins:
        if join.id == join_id and not join.is_cancelled:
            join.cancel()
            return True
    return False


def show_joins(joins: list[Join]) -> None:
    """Вывести список участий."""
    if not joins:
        print("Участий нет")
        return
    for join in joins:
        print(f"[{join.id}] {join}")
