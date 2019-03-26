from authark.application.models import Grant


def test_grant_creation() -> None:
    id_ = "1"
    permission_id = "1"
    role_id = "1"

    grant = Grant(id=id_, permission_id='1', role_id='1')

    assert grant.id == id_
    assert grant.permission_id == permission_id
    assert grant.role_id == role_id
