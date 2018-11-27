from authark.application.models.user import User


def test_user_creation() -> None:
    id_ = "af1209fade"
    username = "tebanep"
    email = "eecheverry@nubark.com"
    name = "Esteban Echeverry Pérez"
    gender = "male"

    user = User(id=id_, username=username, email=email,
                name=name, gender=gender)

    assert user.id == id_
    assert user.username == username
    assert user.email == email
    assert user.name == name
    assert user.gender == gender
