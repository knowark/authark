from authark.app.models.user import User


def test_user_creation() -> None:
    username = "tebanep"
    email = "eecheverry@nubark.com"
    password = "ABC123"

    user = User(username=username, email=email, password=password)

    assert user.username == username
    assert user.email == email
    assert user.password == password
