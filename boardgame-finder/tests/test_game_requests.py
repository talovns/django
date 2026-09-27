from datetime import date

import pytest

from models import Game, GameRequest, Meeting, User
from models.game_requests import (
    add_request,
    filter_requests_by_free_slots,
    find_request,
    get_request_status,
    get_statistics,
    sort_requests,
)

GAME = Game(1, "Каркассон", 2, 5)
AUTHOR = User(1, "Никита", "Москва")


def make_meeting(city="Москва"):
    return Meeting(date(2026, 10, 10), city, "Антикафе")


def test_request_contains_meeting():
    meeting = make_meeting()
    request = GameRequest(1, GAME, AUTHOR, 4, meeting)
    assert request.meeting is meeting
    assert request.game is GAME
    assert request.author is AUTHOR


def test_add_request():
    requests = []
    request = add_request(requests, GAME, AUTHOR, 4, make_meeting())
    assert request is not None
    assert requests == [request]


def test_add_request_rejects_wrong_players_count():
    requests = []
    assert add_request(requests, GAME, AUTHOR, 8, make_meeting()) is None
    assert not requests


def test_free_slots_and_is_open():
    request = GameRequest(1, GAME, AUTHOR, 2, make_meeting(), players_joined=1)
    assert request.free_slots() == 1
    assert request.is_open
    request.add_player()
    assert request.free_slots() == 0
    assert not request.is_open


def test_add_player_to_full_request():
    request = GameRequest(1, GAME, AUTHOR, 2, make_meeting(), players_joined=2)
    with pytest.raises(ValueError):
        request.add_player()


def test_find_request_by_game_and_city():
    requests = []
    add_request(requests, GAME, AUTHOR, 4, make_meeting("Казань"))
    assert len(find_request(requests, "каркас")) == 1
    assert len(find_request(requests, "казань")) == 1
    assert not find_request(requests, "уно")


def test_filter_and_sort_requests():
    small = GameRequest(1, GAME, AUTHOR, 2, make_meeting())
    big = GameRequest(2, GAME, AUTHOR, 5, make_meeting())
    requests = [small, big]
    assert list(filter_requests_by_free_slots(requests, 3)) == [big]
    assert sort_requests(requests) == [big, small]


def test_statistics():
    requests = [
        GameRequest(1, GAME, AUTHOR, 2, make_meeting(), players_joined=2),
        GameRequest(2, GAME, AUTHOR, 4, make_meeting(), players_joined=1),
    ]
    stats = get_statistics(requests)
    assert stats == {"total": 2, "open": 1, "closed": 1, "total_free_slots": 3}


def test_get_request_status():
    assert get_request_status(True) == "Заявка открыта, поиск игроков продолжается"
    assert get_request_status(False) == "Заявка закрыта"
