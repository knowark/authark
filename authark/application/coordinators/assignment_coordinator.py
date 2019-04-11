from typing import Dict
from ..models import Role, Ranking, Policy, Resource, Permission, Grant
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    PolicyRepository, ResourceRepository, PermissionRepository,
    GrantRepository)
from .types import DominionDict, RoleDict


class AssignmentCoordinator:

    def __init__(self, user_repository: UserRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 policy_repository: PolicyRepository,
                 resource_repository: ResourceRepository,
                 permission_repository: PermissionRepository,
                 grant_repository: GrantRepository) -> None:
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.policy_repository = policy_repository
        self.resource_repository = resource_repository
        self.permission_repository = permission_repository
        self.grant_repository = grant_repository

    def assign_policy(self, policy_id: str, resource_id: str) -> bool:
        policy = self.policy_repository.get(policy_id)
        resource = self.resource_repository.get(resource_id)

        permission = Permission(policy_id=policy.id, resource_id=resource.id)
        # Prevent duplicates
        duplicate = self.permission_repository.search([
            ('policy_id', '=', policy.id), ('resource_id', '=', resource.id)
        ])

        if duplicate:
            return False

        self.permission_repository.add(permission)
        return True

    def assign_permission(self, role_id: str, permission_id: str) -> bool:
        role = self.role_repository.get(role_id)
        permission = self.permission_repository.get(permission_id)

        grant = Grant(role_id=role.id, permission_id=permission.id)
        # Prevent duplicates
        duplicate = self.grant_repository.search([
            ('role_id', '=', role.id), ('permission_id', '=', permission.id)
        ])

        if duplicate:
            return False

        self.grant_repository.add(grant)
        return True
