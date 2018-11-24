from typing import Dict
from pytest import fixture, raises
from authark.application.models import Dominion
from authark.application.repositories import ExpressionParser
from authark.application.coordinators import ManagementCoordinator


def test_management_coordinator_instantiation(management_coordinator):
    assert management_coordinator is not None


def test_management_coordinator_create_dominion(management_coordinator):
    dominion_dict = dict(
        id='abc001', name='HR Server', url='https://hr.example.com')
    management_coordinator.create_dominion(dominion_dict)
    assert len(management_coordinator.dominion_repository.items) == 2
    assert 'abc001' in management_coordinator.dominion_repository.items


def test_management_coordinator_remove_dominion(management_coordinator):
    dominion_id = '1'
    management_coordinator.remove_dominion(dominion_id)
    assert len(management_coordinator.dominion_repository.items) == 0


def test_management_coordinator_create_role(management_coordinator):
    role_dict = dict(
        id='2', name='admin', dominion_id='abc001',
        description='Administrator')
    management_coordinator.create_role(role_dict)
    assert len(management_coordinator.role_repository.items) == 2
    assert '2' in management_coordinator.role_repository.items


def test_management_coordinator_remove_role(management_coordinator):
    role_id = '1'
    management_coordinator.remove_role(role_id)
    assert len(management_coordinator.role_repository.items) == 0
