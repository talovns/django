"""Встреча по заявке: когда и где собираются игроки."""

from datetime import date


class Meeting:
    """Встреча игроков: дата, город и место проведения."""

    def __init__(self, meeting_date: date, city: str, place: str) -> None:
        """Создать встречу."""
        self.meeting_date = meeting_date
        self.city = city
        self.place = place

    @classmethod
    def from_data(cls, data: dict) -> "Meeting":
        """Создать встречу из словаря с данными JSON."""
        return cls(date.fromisoformat(data["date"]), data["city"], data["place"])

    def __str__(self) -> str:
        """Вернуть описание встречи."""
        return f"{self.meeting_date.strftime('%d.%m.%Y')}, {self.city}, {self.place}"
