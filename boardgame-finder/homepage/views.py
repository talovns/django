"""Главная страница, общий HTML-каркас и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ: кодировка, заголовок, Bootstrap и навигация."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/games/">Игры</a>
        <a class="nav-link" href="/requests/">Заявки</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание сервиса и ссылки на разделы."""
    content = """
    <h1 class="display-4">Поиск игроков</h1>
    <p class="lead">Сервис поиска компании для настольных игр.</p>
    <p>Основные разделы:</p>
    <a href="/games/" class="btn btn-primary me-2">Игры</a>
    <a href="/requests/" class="btn btn-secondary">Заявки</a>
    """
    return HttpResponse(page("Поиск игроков", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница 404 (работает при DEBUG = False)."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404 – страница не найдена", content), status=404)
