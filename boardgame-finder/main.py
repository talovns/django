"""Точка запуска приложения «Поиск игроков для настольных игр»."""

from pathlib import Path

from models import Game, GameRequest, Join, Meeting, User
from models.game_requests import (
    add_request,
    filter_requests_by_free_slots,
    find_request,
    find_request_by_id,
    get_statistics,
    show_requests,
    sort_requests,
)
from models.games import find_game_by_id, show_games
from models.joins import cancel_join, create_join, show_joins
from models.users import add_user, find_user, find_user_by_id, show_users
from storage import (
    load_games,
    load_joins,
    load_requests,
    load_users,
    save_joins,
    save_requests,
    save_users,
)
from utils import input_date, input_int

DATA_DIR = Path(__file__).resolve().parent / "data"
GAMES_FILE = str(DATA_DIR / "games.json")
USERS_FILE = str(DATA_DIR / "users.json")
REQUESTS_FILE = str(DATA_DIR / "requests.json")
JOINS_FILE = str(DATA_DIR / "joins.json")

MENU = """
=== Поиск игроков для настольных игр ===
1. Показать заявки
2. Найти заявку по игре или городу
3. Заявки со свободными местами
4. Заявки по убыванию свободных мест
5. Статистика по заявкам
6. Создать заявку
7. Присоединиться к заявке
8. Отменить участие
9. Показать участия
10. Показать игры
11. Показать игроков
12. Добавить игрока
13. Найти игрока
0. Выход
"""


def show_statistics(requests: list[GameRequest]) -> None:
    """Вывести статистику по заявкам."""
    stats = get_statistics(requests)
    print(f"Всего заявок: {stats['total']}")
    print(f"Открыто: {stats['open']}")
    print(f"Закрыто: {stats['closed']}")
    print(f"Свободных мест суммарно: {stats['total_free_slots']}")


def handle_find_request(requests: list[GameRequest]) -> None:
    """Обработать поиск заявки по игре или городу."""
    query = input("Название игры или город: ")
    show_requests(find_request(requests, query))


def handle_filter(requests: list[GameRequest]) -> None:
    """Обработать отбор заявок по количеству свободных мест."""
    min_free = input_int("Минимум свободных мест: ")
    show_requests(list(filter_requests_by_free_slots(requests, min_free)))


def handle_create_request(
    requests: list[GameRequest], games: list[Game], users: list[User]
) -> None:
    """Создать заявку: выбрать игру и автора, указать места и встречу."""
    show_games(games)
    game = find_game_by_id(games, input_int("ID игры: "))
    if game is None:
        print("Игра не найдена")
        return
    author = find_user_by_id(users, input_int("ID автора заявки: "))
    if author is None:
        print("Игрок не найден")
        return
    players_needed = input_int("Сколько всего игроков нужно: ")
    meeting = Meeting(
        input_date("Дата встречи (ДД.ММ.ГГГГ): "),
        input("Город: "),
        input("Место встречи: "),
    )
    request = add_request(requests, game, author, players_needed, meeting)
    if request is None:
        print(f"«{game.title}» рассчитана на {game.min_players}-{game.max_players} игроков")
        return
    print(f"Заявка создана, id={request.id}")


def handle_join(requests: list[GameRequest], users: list[User], joins: list[Join]) -> None:
    """Записать игрока в заявку."""
    request = find_request_by_id(requests, input_int("ID заявки: "))
    if request is None:
        print("Заявка не найдена")
        return
    user = find_user_by_id(users, input_int("ID игрока: "))
    if user is None:
        print("Игрок не найден")
        return
    join = create_join(joins, request, user)
    if join is None:
        print("Присоединиться нельзя: мест нет или игрок уже в заявке")
        return
    print(f"Игрок присоединился, id участия={join.id}")


def handle_cancel_join(joins: list[Join]) -> None:
    """Отменить участие игрока."""
    if cancel_join(joins, input_int("ID участия: ")):
        print("Участие отменено")
    else:
        print("Активное участие не найдено")


def handle_add_user(users: list[User]) -> None:
    """Добавить нового игрока."""
    user = add_user(users, input("Имя: "), input("Город: "))
    print(f"Игрок добавлен, id={user.id}")


def handle_find_user(users: list[User]) -> None:
    """Найти игроков по имени или городу."""
    show_users(find_user(users, input("Имя или город: ")))


def save_all(users: list[User], requests: list[GameRequest], joins: list[Join]) -> None:
    """Сохранить все изменяемые данные в JSON."""
    save_users(USERS_FILE, users)
    save_requests(REQUESTS_FILE, requests)
    save_joins(JOINS_FILE, joins)


def main() -> None:
    """Точка запуска приложения: загрузка данных, меню и сохранение."""
    games = load_games(GAMES_FILE)
    users = load_users(USERS_FILE)
    requests = load_requests(REQUESTS_FILE, games, users)
    joins = load_joins(JOINS_FILE, requests, users)

    actions = {
        "1": lambda: show_requests(requests),
        "2": lambda: handle_find_request(requests),
        "3": lambda: handle_filter(requests),
        "4": lambda: show_requests(sort_requests(requests)),
        "5": lambda: show_statistics(requests),
        "6": lambda: handle_create_request(requests, games, users),
        "7": lambda: handle_join(requests, users, joins),
        "8": lambda: handle_cancel_join(joins),
        "9": lambda: show_joins(joins),
        "10": lambda: show_games(games),
        "11": lambda: show_users(users),
        "12": lambda: handle_add_user(users),
        "13": lambda: handle_find_user(users),
    }

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До встречи!")
            break
        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда")
            continue
        action()
        save_all(users, requests, joins)


if __name__ == "__main__":
    main()
