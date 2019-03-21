from authark.application.models import Policy


def test_policy_creation() -> None:
    id_ = "001"
    type = "role"
    name = "Administrators Only"
    value = "admin"

    policy = Policy(id=id_, name=name, type=type, value=value)

    assert policy.id == id_
    assert policy.type == type
    assert policy.name == name
    assert policy.value == value
