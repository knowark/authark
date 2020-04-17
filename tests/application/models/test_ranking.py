from pytest import fixture
from authark.application.models import Ranking


@fixture
def ranking():
    return Ranking(
        id='1',
        user_id='1',
        role_id='1'
    )


def test_ranking_instantiation(ranking):
    assert ranking is not None


def test_ranking_attributes(ranking):
    assert ranking.user_id == '1'
    assert ranking.role_id == '1'
