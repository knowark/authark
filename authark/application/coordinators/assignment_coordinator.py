from typing import Dict
from ..models import Role, Ranking, Policy, Resource, Permission
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    PolicyRepository, ResourceRepository, PermissionRepository)
from .types import DominionDict, RoleDict


class AssignmentCoordinator:

    def __init__(self, user_repository: UserRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 policy_repository: PolicyRepository,
                 resource_repository: ResourceRepository,
                 permission_repository: PermissionRepository) -> None:
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.policy_repository = policy_repository
        self.resource_repository = resource_repository
        self.permission_repository = permission_repository

    def assign_policy(self, policy_id: str, resource_id: str) -> bool:
        policy = self.policy_repository.get(policy_id)
        resource = self.resource_repository.get(resource_id)
        print('DUP>>>', policy.id, resource.id)
        if not (policy and resource):
            return False

        permission = Permission(policy_id=policy.id, resource_id=resource.id)
        # Prevent duplicates
        duplicate = self.permission_repository.search([
            ('policy_id', '=', policy.id), ('resource_id', '=', resource.id)
        ])
        print('DUP>>>', duplicate, policy.id, resource.id)
        if duplicate:
            return False

        self.permission_repository.add(permission)
        return True
