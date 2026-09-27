from datetime import date

from models import Meeting


def test_meeting_creation():
    meeting = Meeting(date(2026, 10, 10), "Москва", "Антикафе")
    assert meeting.city == "Москва"
    assert str(meeting) == "10.10.2026, Москва, Антикафе"


def test_meeting_from_data():
    meeting = Meeting.from_data({"date": "2026-10-10", "city": "Москва", "place": "Клуб"})
    assert meeting.meeting_date == date(2026, 10, 10)
    assert meeting.place == "Клуб"
