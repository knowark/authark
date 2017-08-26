from authark.app.models.user import User


def test_user_creation() -> None:
    uid = "ID001"
    name = "Esteban"
    email = "eecheverry@nubark.com"
    password = "ABC123"

    user = User(uid=uid, name=name, email=email, password=password)

    assert user.uid == uid
    assert user.name == name
    assert user.email == email
    assert user.password == password
