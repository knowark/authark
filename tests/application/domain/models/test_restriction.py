from pytest import fixture
from authark.application.domain.models import Restriction


@fixture
def restriction():
    return Restriction(
        id="1",
        policy_id="1",
        name="Restriction name",
        sequence=1,
        target="Target name",
        domain="domain"
    )


def test_restriction_instation(restriction):
    assert restriction is not None


def test_restriction_attributes(restriction):
    assert restriction.id == "1"
    assert restriction.policy_id == "1"
    assert restriction.name == "Restriction name"
    assert restriction.sequence == 1
    assert restriction.target == "Target name"
    assert restriction.domain == "domain"
