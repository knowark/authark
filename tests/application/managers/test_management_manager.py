from authark.application.domain.common import RecordList


def test_management_manager_instantiation(management_manager):
    assert management_manager is not None


async def test_management_manager_create_dominion(management_manager):
    dominion_dicts: RecordList = [{
        "id": 'abc001',
        "name": 'HR Server',
        "url": 'https://hr.example.com'
    }]
    await management_manager.create_dominion(dominion_dicts)
    assert len(
        management_manager.dominion_repository.data['default']) == 2
    assert 'abc001' in management_manager.dominion_repository.data[
        'default']


async def test_management_manager_remove_dominion(management_manager):
    dominion_ids = ['1']
    await management_manager.remove_dominion(dominion_ids)
    assert len(management_manager.dominion_repository.data[
        'default']) == 0


async def test_management_manager_create_role(management_manager):
    role_dicts: RecordList = [{
        "id": '2',
        "name": 'admin',
        "dominion_id": 'abc001',
        "description": 'Administrator'
    }]
    await management_manager.create_role(role_dicts)
    assert len(management_manager.role_repository.data['default']) == 2
    assert '2' in management_manager.role_repository.data['default']


async def test_management_manager_remove_role(management_manager):
    role_ids = ['1']
    await management_manager.remove_role(role_ids)
    assert len(management_manager.role_repository.data['default']) == 0


async def test_management_manager_assign_role(management_manager):
    ranking_dicts = [{'user_id': '3', 'role_id': '1'}]
    await management_manager.assign_role(ranking_dicts)
    assert len(management_manager.ranking_repository.data['default']) == 3


async def test_management_manager_assign_role_duplicate(management_manager):
    ranking_dicts = [{'user_id': '1', 'role_id': '1'}]
    await management_manager.assign_role(ranking_dicts)
    assert len(management_manager.ranking_repository.data['default']) == 2


async def test_management_manager_deassign_role(management_manager):
    ranking_ids = ['1']
    await management_manager.deassign_role(ranking_ids)
    assert len(management_manager.ranking_repository.data['default']) == 1
