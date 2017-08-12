from authark.app.models.user import User, UserContainer


def test_user_creation() -> None:
    name = "Esteban"
    email = "eecheverry@nubark.com"
    user = User(name=name, email=email)

    assert user.name == name
    assert user.email == email


def test_user_container() -> None:
    methods = UserContainer.__abstractmethods__
    assert 'get' in methods
