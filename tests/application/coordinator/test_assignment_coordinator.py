from typing import Dict
from pytest import fixture, raises
from authark.application.models import Dominion
from authark.application.repositories import ExpressionParser
from authark.application.coordinators import ManagementCoordinator


def test_assignment_coordinator_instantiation(assignment_coordinator):
    assert assignment_coordinator is not None


def test_assignment_coordinator_assign_policy(assignment_coordinator):
    policy_id = '001'
    resource_id = '001'
    assignment_coordinator.assign_policy(policy_id, resource_id)
    assert len(assignment_coordinator.permission_repository.items) == 2


def test_management_coordinator_assign_policy_missing_id(
        assignment_coordinator):
    policy_id = '001'
    resource_id = '999'
    result = assignment_coordinator.assign_policy(policy_id, resource_id)
    assert result is False
    assert len(assignment_coordinator.permission_repository.items) == 1


def test_management_coordinator_assign_policy_duplicate(
        assignment_coordinator):
    policy_id = '002'
    resource_id = '002'
    assignment_coordinator.permission_repository.items['2'] = (
        Permission(id='2', policy_id='002', resource_id='002')
    )

    assignment_coordinator.assign_policy(policy_id, resource_id)
    assert len(assignment_coordinator.permission_repository.items) == 2
