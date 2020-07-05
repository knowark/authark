from pytest import fixture
from authark.application.domain.models import Policy


@fixture
def policy():
    return Policy(
        id="1",
        resource="Resource name",
        privilege="Privilege name",
        role_id="1",
        restriction="Restriction name",
    )


def test_policy_creation(policy):
    assert policy is not None


def test_policy_attributes(policy):
    assert policy.id == "1"
    assert policy.resource == "Resource name"
    assert policy.active is False
    assert policy.privilege == "Privilege name"
    assert policy.role_id == "1"
    assert policy.restriction == "Restriction name"
