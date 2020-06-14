from pytest import fixture
from authark.application.domain.models import Policy

@fixture
def policy():
    return Policy(
        id_ = "1",
        resource = "Resource name",
        privilege = "Privilege name",
        role = "Role name",
        rule = "Rule name",
    )

def test_policy_creation(policy):
    assert policy is not None


def test_policy_attributes(policy):
    # assert policy.id == "1"
    assert policy.resource == "Resource name"
    assert policy.privilege == "Privilege name"
    assert policy.role == "Role name"
    assert policy.rule == "Rule name"
