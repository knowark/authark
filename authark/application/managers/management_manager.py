from typing import List
from ..domain.models import Dominion, Role, Ranking
from ..domain.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from ..domain.common import RecordList


class ManagementManager:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def create_dominion(self, dominion_dicts: RecordList) -> None:
        dominions = ([Dominion(**dominion_dict)
                      for dominion_dict in dominion_dicts])
        await self.dominion_repository.add(dominions)

    async def remove_dominion(self, dominion_ids: List[str]) -> bool:
        dominions = await self.dominion_repository.search(
            [('id', 'in', dominion_ids)])
        return await self.dominion_repository.remove(dominions)

    async def create_role(self, role_dicts: RecordList) -> None:
        roles = [Role(**role_dict) for role_dict in role_dicts]
        await self.role_repository.add(roles)

    async def remove_role(self, role_ids: List[str]) -> bool:
        roles = await self.role_repository.search(
            [('id', 'in', role_ids)])
        return await self.role_repository.remove(roles)
    
    # async def create_ranking(self, ranking_dicts: RecordList) -> None:
    #     existing_users = await self.user_repository.search(
    #         [('id', 'in', ranking_dicts[0]['user_id'])])
    #     existing_roles = await self.role_repository.search([
    #         [('id', 'in', ranking_dicts[1]['role_id'])

    #     if existing_users and existing_roles:
    #         rankings = [Ranking(**ranking_dict) for ranking_dict in ranking_dicts]
    #     return await self.role_repository.add(rankings)

    async def assign_role(self, ranking_dicts: RecordList) -> None:
        user_set = {
            item.id for item in await self.user_repository.search([
                ('id', 'in', [
                    record['user_id'] for record in ranking_dicts])])
        }

        role_set = {
            item.id for item in await self.role_repository.search([
                ('id', 'in', [
                    record['role_id'] for record in ranking_dicts])])
        }

        rankings = [
            Ranking(**record) for record in ranking_dicts
            if record['user_id'] in user_set and
            record['role_id'] in role_set]

        existing_rankings = await self.ranking_repository.search([
            '|', ('user_id', 'in',  [ranking.user_id for ranking in rankings]),
            ('role_id', 'in',  [ranking.role_id for ranking in rankings])
        ])

        # Check for duplicates
        for existing_ranking in existing_rankings:
            for ranking in rankings:
                if (existing_ranking.user_id == ranking.user_id and
                        existing_ranking.role_id == ranking.role_id):
                    ranking.id = existing_ranking.id

        await self.ranking_repository.add(rankings)

    async def deassign_role(self, ranking_ids: List[str]) -> bool:
        rankings = await self.ranking_repository.search(
            [('id', 'in', ranking_ids)])
        return await self.ranking_repository.remove(rankings)
