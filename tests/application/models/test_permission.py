from authark.application.models import Permission


def test_permission_creation() -> None:
    id_ = "1"
    policy_id = "1"
    resource_id = "1"

    permission = Permission(id=id_, policy_id='1', resource_id='1')

    assert permission.id == id_
    assert permission.policy_id == policy_id
    assert permission.resource_id == resource_id
