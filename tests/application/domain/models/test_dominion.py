from pytest import fixture
from authark.application.domain.models import Dominion


@fixture
def dominion():
    return Dominion(name='superapp')


def test_dominion_instation(dominion):
    assert dominion is not None


def test_dominion_attributes(dominion):
    assert dominion.name == 'superapp'
