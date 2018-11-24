from authark.application.models import Ranking


def test_ranking_creation() -> None:
    id_ = "1"
    user_id = "1"
    role_id = "1"

    ranking = Ranking(id=id_, user_id='1', role_id='1')

    assert ranking.id == id_
    assert ranking.user_id == user_id
    assert ranking.role_id == role_id
