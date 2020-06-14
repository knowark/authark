from pytest import fixture
from authark.application.domain.models import Rule


@fixture
def rule():
    return Rule(
        id_ = "1",
        group = "Group name",
        name = "Rule name",
        sequence = "1",
        target = "Target name",
        domain = "domain"
    )

def test_rule_instation(rule):
    assert rule is not None


def test_rule_attributes(rule):
    # assert rule.id == "1"
    assert rule.group == "Group name"
    assert rule.name == "Rule name"
    assert rule.sequence == "1"
    assert rule.target == "Target name"
    assert rule.domain == "domain"
