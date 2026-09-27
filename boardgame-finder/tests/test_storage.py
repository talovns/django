from datetime import date

from models import Game, Meeting, User
from models.game_requests import add_request
from models.joins import create_join
from storage import load_joins, load_requests, load_users, save_joins, save_requests


def test_save_and_load_restores_links(tmp_path):
    game = Game(1, "Каркассон", 2, 5)
    author = User(1, "Никита", "Москва")
    player = User(2, "Аня", "Москва")
    requests = []
    meeting = Meeting(date(2026, 10, 10), "Москва", "Клуб")
    request = add_request(requests, game, author, 4, meeting)
    assert request is not None
    joins = []
    create_join(joins, request, player)

    requests_file = str(tmp_path / "requests.json")
    joins_file = str(tmp_path / "joins.json")
    save_requests(requests_file, requests)
    save_joins(joins_file, joins)

    loaded_requests = load_requests(requests_file, [game], [author, player])
    loaded_joins = load_joins(joins_file, loaded_requests, [author, player])
    assert loaded_requests[0].game is game
    assert loaded_requests[0].meeting.place == "Клуб"
    assert loaded_requests[0].players_joined == 1
    assert loaded_joins[0].request is loaded_requests[0]
    assert loaded_joins[0].user is player


def test_load_missing_file(tmp_path):
    assert not load_users(str(tmp_path / "missing.json"))
