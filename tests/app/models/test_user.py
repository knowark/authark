from authark.app.models.user import User


def test_user_creation() -> None:
    name = "Esteban"
    email = "eecheverry@nubark.com"
    user = User(name=name, email=email)

    assert user.name == name
    assert user.email == email
