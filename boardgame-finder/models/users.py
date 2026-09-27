"""Игроки: класс User и функции работы с коллекцией игроков."""

from typing import Optional


class User:
    """Игрок, пользователь сервиса."""

    def __init__(self, user_id: int, name: str, city: str) -> None:
        """Создать игрока."""
        self.id = user_id
        self.name = name
        self.city = city

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать игрока из словаря с данными JSON."""
        return cls(data["id"], data["name"], data["city"])

    def __str__(self) -> str:
        """Вернуть описание игрока."""
        return f"{self.name} ({self.city})"


def add_user(users: list[User], name: str, city: str) -> User:
    """Создать игрока, добавить его в коллекцию и вернуть."""
    user_id = max((user.id for user in users), default=0) + 1
    user = User(user_id, name, city)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти игроков по подстроке в имени или городе."""
    query_lower = query.lower()
    return [
        user for user in users
        if query_lower in user.name.lower() or query_lower in user.city.lower()
    ]


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    """Найти игрока по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[User]) -> None:
    """Вывести список игроков."""
    if not users:
        print("Игроков нет")
        return
    for user in users:
        print(f"[{user.id}] {user}")
