# from authark.application.domain.models import Rule, Policy
from authark.application.managers import SecurityManager
from authark.application.domain.common import RecordList


def test_security_manager_instantiation(security_manager):
    assert security_manager is not None


async def test_security_manager_create_rule(security_manager):
    rule_dicts: RecordList = [{
        "id": '1',
    }]
    await security_manager.create_rule(rule_dicts)
    assert len(
        security_manager.rule_repository.data['default']) == 1
    assert '1' in security_manager.rule_repository.data[
        'default']


async def test_security_manager_create_policy(security_manager):
    policy_dicts: RecordList = [{
        "id": '1',
    }]
    await security_manager.create_policy(policy_dicts)
    assert len(
        security_manager.policy_repository.data['default']) == 1
    assert '1' in security_manager.policy_repository.data[
        'default']


async def test_management_manager_remove_rule(security_manager):
    rule_ids = ['1']
    await security_manager.remove_rule(rule_ids)
    assert len(security_manager.rule_repository.data[
        'default']) == 1


async def test_management_manager_remove_policy(security_manager):
    policy_ids = ['1']
    await security_manager.remove_policy(policy_ids)
    assert len(security_manager.policy_repository.data[
        'default']) == 1
