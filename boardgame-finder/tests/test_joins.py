from datetime import date

from models import Game, GameRequest, Join, Meeting, User
from models.joins import can_join_request, cancel_join, create_join


def make_request(players_needed=2):
    game = Game(1, "Каркассон", 2, 5)
    author = User(1, "Никита", "Москва")
    meeting = Meeting(date(2026, 10, 10), "Москва", "Антикафе")
    return GameRequest(1, game, author, players_needed, meeting)


def test_join_links_objects():
    request = make_request()
    user = User(2, "Аня", "Москва")
    join = Join(1, request, user)
    assert join.request is request
    assert join.user is user
    assert not join.is_cancelled


def test_create_join_takes_slot():
    request = make_request()
    joins = []
    join = create_join(joins, request, User(2, "Аня", "Москва"))
    assert join is not None
    assert joins == [join]
    assert request.players_joined == 1


def test_duplicate_join_forbidden():
    request = make_request()
    user = User(2, "Аня", "Москва")
    joins = []
    create_join(joins, request, user)
    assert not can_join_request(joins, request, user)
    assert create_join(joins, request, user) is None


def test_full_request_blocks_join():
    request = make_request(players_needed=1)
    joins = []
    create_join(joins, request, User(2, "Аня", "Москва"))
    assert create_join(joins, request, User(3, "Борис", "Москва")) is None


def test_cancel_frees_slot_and_keeps_join():
    request = make_request(players_needed=1)
    user = User(2, "Аня", "Москва")
    joins = []
    join = create_join(joins, request, user)
    assert join is not None
    assert cancel_join(joins, join.id)
    assert join.is_cancelled
    assert joins == [join]
    assert request.is_open
    assert create_join(joins, request, user) is not None


def test_cancel_unknown_join():
    assert not cancel_join([], 99)
