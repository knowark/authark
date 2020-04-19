from typing import Dict, List
from ..models import Dominion, Role, Ranking
from ..repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from ..utilities.types import RecordList


class ManagementCoordinator:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def create_dominion(self, dominion_dicts: RecordList) -> None:
        dominions = ([
            Dominion(**dominion_dict)
            for dominion_dict in dominion_dicts])
        await self.dominion_repository.add(dominions)

    async def remove_dominion(self, dominion_ids: List[str]) -> bool:
        dominions = await self.dominion_repository.search(
            [('id', 'in', dominion_ids)])
        await self.dominion_repository.remove(dominions)
        return True

    async def create_role(self, role_dicts: RecordList) -> None:
        roles = ([
            Role(**role_dict)
            for role_dict in role_dicts])
        await self.role_repository.add(roles)

    async def remove_role(self, role_ids: List[str]) -> bool:
        roles = await self.dominion_repository.search(
            [('id', 'in', role_ids)])
        await self.role_repository.remove(roles)
        return True

    async def assign_role(
            self, user_ids: str, role_ids: List[str]) -> bool:
        users = await self.user_repository.search(
            [('id', 'in', user_ids)])
        roles = await self.role_repository.search(
            [('id', 'in', role_ids)])
        for i in range(len(users)):
            rankings = Ranking(user_id=users[i].id, role_id=roles[i].id)
        duplicates = await self.ranking_repository.search([
            ('user_id', '=', users[i].id), ('role_id', '=', roles[i].id)])
        if duplicates:
            return False

        await self.ranking_repository.add(rankings)
        return True

    async def deassign_role(self, ranking_ids: List[str]) -> bool:
        rankings = await self.ranking_repository.search(
            [('id', 'in', ranking_ids)])
        return await self.ranking_repository.remove(rankings)
