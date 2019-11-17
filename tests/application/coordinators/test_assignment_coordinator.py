from typing import Dict
from pytest import fixture, raises
from authark.application.models import Permission
from authark.application.utilities import ExpressionParser
from authark.application.coordinators import ManagementCoordinator


def test_assignment_coordinator_instantiation(assignment_coordinator):
    assert assignment_coordinator is not None


def test_assignment_coordinator_assign_policy(assignment_coordinator):
    policy_id = '001'
    resource_id = '1'
    assignment_coordinator.permission_repository.data = {"default": {}}
    assignment_coordinator.assign_policy(policy_id, resource_id)
    assert len(
        assignment_coordinator.permission_repository.data['default']) == 1


def test_assignment_coordinator_assign_policy_duplicate(
        assignment_coordinator):
    policy_id = '001'
    resource_id = '1'
    assignment_coordinator.permission_repository.data['default']['001'] = (
        Permission(id='001', policy_id='001', resource_id='1')
    )

    assignment_coordinator.assign_policy(policy_id, resource_id)
    assert len(
        assignment_coordinator.permission_repository.data['default']) == 1
