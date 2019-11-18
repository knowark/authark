from typing import Dict
from ..models import Dominion, Role, Ranking, Resource
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    ResourceRepository)
from .types import DominionDict, RoleDict


class ManagementCoordinator:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 resource_repository: ResourceRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.resource_repository = resource_repository

    def create_dominion(self, dominion_dict: DominionDict) -> None:
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)

    def remove_dominion(self, dominion_id: str) -> bool:
        dominion = self.dominion_repository.get(dominion_id)
        self.dominion_repository.remove(dominion)
        return True

    def create_resource(self, dominion_dict: DominionDict) -> None:
        resource = Resource(**dominion_dict)
        self.resource_repository.add(resource)

    def remove_resource(self, resource_id: str) -> bool:
        resource = self.resource_repository.get(resource_id)
        self.resource_repository.remove(resource)
        return True

    def create_role(self, role_dict: RoleDict) -> None:
        role = Role(**role_dict)
        self.role_repository.add(role)

    def remove_role(self, role_id: str) -> bool:
        role = self.role_repository.get(role_id)
        self.role_repository.remove(role)
        return True

    def assign_role(self, user_id: str, role_id: str) -> bool:
        user = self.user_repository.get(user_id)
        role = self.role_repository.get(role_id)

        ranking = Ranking(user_id=user.id, role_id=role.id)
        duplicate = self.ranking_repository.search([
            ('user_id', '=', user.id), ('role_id', '=', role.id)
        ])
        if duplicate:
            return False

        self.ranking_repository.add(ranking)
        return True

    def deassign_role(self, ranking_id: str) -> bool:
        ranking = self.ranking_repository.get(ranking_id)
        return self.ranking_repository.remove(ranking)
