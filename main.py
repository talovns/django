"""Начальный сценарий проекта «Сервис поиска игроков для настольных игр»."""

from datetime import date

# --- Данные заявки на поиск игроков ---
game_title = "Каркассон"
city = "Москва"
players_needed = 4
players_joined = 2
is_request_open = True
meeting_date = date(2026, 9, 20)


def get_request_status(is_open):
    """Определяет текстовый статус заявки по логическому флагу."""
    if is_open:
        return "Заявка открыта, поиск игроков продолжается"
    else:
        return "Заявка закрыта"


def calculate_free_slots(needed, joined):
    """Вычисляет количество свободных мест на встрече."""
    free_slots = needed - joined
    if free_slots < 0:
        return 0
    return free_slots


def can_join_meeting(free_slots):
    """Проверяет, можно ли ещё присоединиться к встрече."""
    return free_slots > 0


def format_meeting_info(title, meeting_city, meeting_date, free_slots):
    """Формирует текстовое описание встречи для участников."""
    date_text = meeting_date.strftime("%d.%m.%Y")
    slots_text = str(free_slots)
    return (
        "Игра «" + title + "» в городе " + meeting_city +
        " состоится " + date_text + ". Свободных мест: " + slots_text
    )


free_slots = calculate_free_slots(players_needed, players_joined)

print(f"Игра: {game_title}")
print(f"Город: {city}")
print(f"Нужно игроков: {players_needed}")
print(f"Уже присоединилось: {players_joined}")
print(get_request_status(is_request_open))
print(format_meeting_info(game_title, city, meeting_date, free_slots))

if can_join_meeting(free_slots):
    print("Можно присоединиться к встрече")
else:
    print("Свободных мест нет")
