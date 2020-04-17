from pytest import fixture
from authark.application.models import Role


@fixture
def role():
    return Role(
        id='1',
        name='admin',
        dominion_id='1',
        description='Systems Administrator'
    )


def test_role_instantiation(role):
    assert role is not None


def test_role_attributes(role):
    assert role.name == 'admin'
    assert role.dominion_id == '1'
    assert role.description == 'Systems Administrator'
