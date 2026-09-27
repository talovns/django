from models import Game
from models.games import find_game_by_id


def test_game_creation():
    game = Game(1, "Каркассон", 2, 5)
    assert game.id == 1
    assert game.title == "Каркассон"
    assert str(game) == "Каркассон (2-5 игроков)"


def test_game_supports_players():
    game = Game(1, "Колонизаторы", 3, 4)
    assert game.supports_players(3)
    assert not game.supports_players(2)
    assert not game.supports_players(5)


def test_game_from_data():
    game = Game.from_data({"id": 2, "title": "Уно", "min_players": 2, "max_players": 10})
    assert game.title == "Уно"
    assert game.max_players == 10


def test_find_game_by_id():
    games = [Game(1, "Каркассон", 2, 5), Game(2, "Уно", 2, 10)]
    assert find_game_by_id(games, 2) is games[1]
    assert find_game_by_id(games, 99) is None
