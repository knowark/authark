from typing import Dict
from ..models import Dominion, Role, Ranking, Policy, Resource
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    PolicyRepository, ResourceRepository)
from .types import DominionDict, RoleDict


class ManagementCoordinator:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 policy_repository: PolicyRepository,
                 resource_repository: ResourceRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.policy_repository = policy_repository
        self.resource_repository = resource_repository

    def create_dominion(self, dominion_dict: DominionDict) -> None:
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)

    def remove_dominion(self, dominion_id: str) -> bool:
        dominion = self.dominion_repository.get(dominion_id)
        if not dominion:
            return False
        self.dominion_repository.remove(dominion)
        return True

    def create_resource(self, dominion_dict: DominionDict) -> None:
        resource = Resource(**dominion_dict)
        self.resource_repository.add(resource)

    def remove_resource(self, resource_id: str) -> bool:
        resource = self.resource_repository.get(resource_id)
        if not resource:
            return False
        self.resource_repository.remove(resource)
        return True

    def create_policy(self, policy_dict: Dict[str, str]) -> None:
        policy = Policy(**policy_dict)
        self.policy_repository.add(policy)

    def remove_policy(self, policy_id: str) -> bool:
        policy = self.policy_repository.get(policy_id)
        if not policy:
            return False
        self.policy_repository.remove(policy)
        return True

    def create_role(self, role_dict: RoleDict) -> None:
        role = Role(**role_dict)
        self.role_repository.add(role)

    def remove_role(self, role_id: str) -> bool:
        role = self.role_repository.get(role_id)
        if not role:
            return False
        self.role_repository.remove(role)
        return True

    def assign_role(self, user_id: str, role_id: str) -> bool:
        user = self.user_repository.get(user_id)
        role = self.role_repository.get(role_id)
        if not (user and role):
            return False

        ranking = Ranking(user_id=user.id, role_id=role.id)
        # Prevent duplicates
        duplicate = self.ranking_repository.search([
            ('user_id', '=', user.id), ('role_id', '=', role.id)
        ])
        if duplicate:
            return False

        self.ranking_repository.add(ranking)
        return True

    def deassign_role(self, ranking_id: str) -> bool:
        ranking = self.ranking_repository.get(ranking_id)
        if not ranking:
            return False
        return self.ranking_repository.remove(ranking)
