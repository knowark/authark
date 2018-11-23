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


def test_management_coordinator_create_dominion_no_id(management_coordinator):
    dominion_dict = dict(
        name='HR Server', url='https://hr.example.com')
    management_coordinator.create_dominion(dominion_dict)
    assert len(management_coordinator.dominion_repository.items) == 2
    for item in management_coordinator.dominion_repository.items.values():
        assert len(item.id) > 0
