import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boardgame_finder.settings")
django.setup()


@pytest.fixture(scope="module")
def client():
    from django.test import Client
    from django.test.utils import (
        setup_test_environment,
        teardown_test_environment,
    )

    setup_test_environment()
    yield Client()
    teardown_test_environment()


@pytest.mark.parametrize("url", ["/", "/games/", "/games/1/", "/requests/", "/requests/1/"])
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


@pytest.mark.parametrize("url", ["/games/999/", "/requests/999/", "/nonexistent/"])
def test_missing_objects_return_404(client, url):
    assert client.get(url).status_code == 404


def test_text_id_is_not_routed(client):
    assert client.get("/games/abc/").status_code == 404


def test_game_list_shows_games(client):
    content = client.get("/games/").content.decode()
    assert "Каркассон" in content
    assert "Колонизаторы" in content


def test_request_detail_shows_linked_objects(client):
    content = client.get("/requests/1/").content.decode()
    assert "Каркассон" in content
    assert "Никита" in content
    assert "Антикафе на Арбате" in content
    assert "Аня" in content
