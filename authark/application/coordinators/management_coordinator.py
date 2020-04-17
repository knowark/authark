from typing import Dict
from ..models import Dominion, Role, Ranking
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from .types import DominionDict, RoleDict


class ManagementCoordinator:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def create_dominion(self, dominion_dict: DominionDict) -> None:
        dominion = Dominion(**dominion_dict)
        await self.dominion_repository.add(dominion)

    async def remove_dominion(self, dominion_id: str) -> bool:
        dominion = await self.dominion_repository.search(dominion_id)
        await self.dominion_repository.remove(dominion)
        return True

    async def create_role(self, role_dict: RoleDict) -> None:
        role = Role(**role_dict)
        await self.role_repository.add(role)

    async def remove_role(self, role_id: str) -> bool:
        role = await self.role_repository.search(role_id)
        await self.role_repository.remove(role)
        return True

    async def assign_role(self, user_id: str, role_id: str) -> bool:
        user = await self.user_repository.search(user_id)
        role = await self.role_repository.search(role_id)

        ranking = Ranking(user_id=user.id, role_id=role.id)
        duplicate = await self.ranking_repository.search([
            ('user_id', '=', user.id), ('role_id', '=', role.id)
        ])
        if duplicate:
            return False

        await self.ranking_repository.add(ranking)
        return True

    async def deassign_role(self, ranking_id: str) -> bool:
        ranking = await self.ranking_repository.search(ranking_id)
        return await self.ranking_repository.remove(ranking)
