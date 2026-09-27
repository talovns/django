from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Никита", "Москва")
    assert user.id == 1
    assert user.name == "Никита"
    assert str(user) == "Никита (Москва)"


def test_user_from_data():
    user = User.from_data({"id": 3, "name": "Аня", "city": "Казань"})
    assert user.id == 3
    assert user.city == "Казань"


def test_add_user():
    users = []
    user = add_user(users, "Борис", "Москва")
    assert users == [user]
    assert user.id == 1


def test_find_user():
    users = [User(1, "Никита", "Москва"), User(2, "Аня", "Казань")]
    assert find_user(users, "казань") == [users[1]]
    assert find_user_by_id(users, 1) is users[0]
