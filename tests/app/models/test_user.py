from authark.app.models.user import User


def test_user_creation() -> None:
    uid = "ID001"
    name = "Esteban"
    email = "eecheverry@nubark.com"
    user = User(uid=uid, name=name, email=email)

    assert user.uid == uid
    assert user.name == name
    assert user.email == email
