from pytest import fixture
from authark.application.models.user import User


def test_user_creation_default():
    user = User(
        username="tebanep",
        email="eecheverry@nubark.com")

    assert user.id == ""
    assert user.username == "tebanep"
    assert user.attributes == {}
    assert user.email == "eecheverry@nubark.com"
    assert user.name == ""


def test_user_creation() -> None:
    user = User(
        id="af1209fade",
        username="tebanep",
        email="eecheverry@nubark.com",
        name="Esteban Echeverry Pérez",
        attributes={
            'key_1': 'value_1',
            'key_2': 'value_2'
        })

    assert user.id == "af1209fade"
    assert user.username == "tebanep"
    assert user.email == "eecheverry@nubark.com"
    assert user.name == "Esteban Echeverry Pérez"
    assert user.attributes == {
        'key_1': 'value_1',
        'key_2': 'value_2'
    }
