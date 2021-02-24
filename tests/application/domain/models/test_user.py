from pytest import fixture
from authark.application.domain.models.user import User


@fixture
def user():
    return User(
        id='af1209fade',
        username='tebanep',
        email='eecheverry@nubark.com',
        name='Esteban Echeverry Pérez',
        active=False,
        attributes={
            'key_1': 'value_1',
            'key_2': 'value_2'
        }
    )


def test_user_instantiation(user):
    assert user is not None


def test_user_attributes(user):
    assert user.username == 'tebanep'
    assert user.email == 'eecheverry@nubark.com'
    assert user.name == 'Esteban Echeverry Pérez'
    assert user.active is False
    assert user.attributes == {
        'key_1': 'value_1',
        'key_2': 'value_2'
    }
