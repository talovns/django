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


def template_names(response):
    return [template.name for template in response.templates]


@pytest.mark.parametrize(
    ("url", "template"),
    [
        ("/", "homepage/index.html"),
        ("/games/", "games/game_list.html"),
        ("/games/1/", "games/game_detail.html"),
        ("/requests/", "gamerequests/request_list.html"),
        ("/requests/1/", "gamerequests/request_detail.html"),
    ],
)
def test_pages_use_templates(client, url, template):
    names = template_names(client.get(url))
    assert template in names
    assert "base.html" in names
    assert "includes/navigation.html" in names


def test_includes_are_used(client):
    assert "games/includes/game_card.html" in template_names(client.get("/games/"))
    names = template_names(client.get("/requests/1/"))
    assert "gamerequests/includes/request_status.html" in names


def test_missing_object_uses_template_message(client):
    response = client.get("/requests/999/")
    assert response.status_code == 404
    assert "Заявка не найдена" in response.content.decode()


def test_static_files_are_linked(client):
    content = client.get("/").content.decode()
    assert "/static/homepage/css/style.css" in content
    assert "/static/homepage/js/main.js" in content
    assert "/static/homepage/img/logo.svg" in content


def test_date_filter_formats_meeting_date(client):
    assert "10.10.2026" in client.get("/requests/").content.decode()


def test_page_helper_removed():
    import homepage.views

    assert not hasattr(homepage.views, "page")
