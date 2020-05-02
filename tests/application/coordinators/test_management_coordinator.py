from typing import Dict
from pytest import fixture, raises
from authark.application.models import Dominion
from authark.application.utilities import QueryParser, RecordList
from authark.application.coordinators import ManagementCoordinator


def test_management_coordinator_instantiation(
        management_coordinator: ManagementCoordinator) -> None:
    assert management_coordinator is not None


async def test_management_coordinator_create_dominion(
        management_coordinator: ManagementCoordinator) -> None:
    dominion_dicts: RecordList = [{
        "id": 'abc001',
        "name": 'HR Server',
        "url": 'https://hr.example.com'
    }]
    await management_coordinator.create_dominion(dominion_dicts)
    assert len(management_coordinator.dominion_repository.data[
        'default']) == 2
    assert 'abc001' in management_coordinator.dominion_repository.data[
        'default']


async def test_management_coordinator_remove_dominion(
        management_coordinator: ManagementCoordinator) -> None:
    dominion_ids = ['1']
    await management_coordinator.remove_dominion(dominion_ids)
    assert len(management_coordinator.dominion_repository.data[
        'default']) == 0


async def test_management_coordinator_create_role(
        management_coordinator: ManagementCoordinator) -> None:
    role_dicts: RecordList = [{
        "id": '2',
        "name": 'admin',
        "dominion_id": 'abc001',
        "description": 'Administrator'
    }]
    await management_coordinator.create_role(role_dicts)
    assert len(management_coordinator.role_repository.data['default']) == 2
    assert '2' in management_coordinator.role_repository.data['default']


async def test_management_coordinator_remove_role(
        management_coordinator: ManagementCoordinator) -> None:
    role_ids = ['1']
    await management_coordinator.remove_role(role_ids)
    assert len(management_coordinator.role_repository.data['default']) == 0


async def test_management_coordinator_assign_role(
        management_coordinator: ManagementCoordinator) -> None:
    user_ids = ['2']
    role_ids = ['1']
    await management_coordinator.assign_role(user_ids, role_ids)
    assert len(management_coordinator.ranking_repository.data['default']) == 3


async def test_management_coordinator_assign_role_duplicate(
        management_coordinator: ManagementCoordinator) -> None:
    user_ids = ['1']
    role_ids = ['1']
    await management_coordinator.assign_role(user_ids, role_ids)
    assert len(management_coordinator.ranking_repository.data['default']) == 2


async def test_management_coordinator_deassign_role(
        management_coordinator: ManagementCoordinator) -> None:
    ranking_ids = ['1']
    await management_coordinator.deassign_role(ranking_ids)
    assert len(management_coordinator.ranking_repository.data['default']) == 1
