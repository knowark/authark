from authark.application.models.user import User


def test_user_creation() -> None:
    id_ = "af1209fade"
    username = "tebanep"
    email = "eecheverry@nubark.com"
    password = "ABC123"

    user = User(id=id_, username=username, email=email)

    assert user.id == id_
    assert user.username == username
    assert user.email == email
