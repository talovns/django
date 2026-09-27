"""Настольные игры: класс Game и функции работы с каталогом игр."""

from typing import Optional


class Game:
    """Настольная игра из каталога."""

    def __init__(self, game_id: int, title: str, min_players: int, max_players: int) -> None:
        """Создать игру."""
        self.id = game_id
        self.title = title
        self.min_players = min_players
        self.max_players = max_players

    def supports_players(self, players_count: int) -> bool:
        """Проверить, можно ли играть в игру указанным числом игроков."""
        return self.min_players <= players_count <= self.max_players

    @classmethod
    def from_data(cls, data: dict) -> "Game":
        """Создать игру из словаря с данными JSON."""
        return cls(data["id"], data["title"], data["min_players"], data["max_players"])

    def __str__(self) -> str:
        """Вернуть описание игры."""
        return f"{self.title} ({self.min_players}-{self.max_players} игроков)"


def find_game_by_id(games: list[Game], game_id: int) -> Optional[Game]:
    """Найти игру по идентификатору."""
    for game in games:
        if game.id == game_id:
            return game
    return None


def show_games(games: list[Game]) -> None:
    """Вывести каталог игр."""
    if not games:
        print("Игр нет")
        return
    for game in games:
        print(f"[{game.id}] {game}")
