from typing import List
from ...domain.models import Dominion, Role, Ranking
from ...domain.services.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from ...domain.common import RecordList


class ManagementManager:

    def __init__(self, user_repository: UserRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def create_dominion(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        dominion_dicts = data
        dominions = ([Dominion(**dominion_dict)
                      for dominion_dict in dominion_dicts])
        await self.dominion_repository.add(dominions)

        return {}

    async def remove_dominion(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        dominion_ids = data
        dominions = await self.dominion_repository.search(
            [('id', 'in', dominion_ids)])
        return {"data": await self.dominion_repository.remove(dominions)}

    async def create_role(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        role_dicts = data
        roles = [Role(**role_dict) for role_dict in role_dicts]
        await self.role_repository.add(roles)

        return {}

    async def remove_role(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        role_ids = data
        roles = await self.role_repository.search(
            [('id', 'in', role_ids)])
        return {"data": await self.role_repository.remove(roles)}

    async def assign_role(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        ranking_dicts = data
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

        return {}

    async def deassign_role(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        ranking_ids = data
        rankings = await self.ranking_repository.search(
            [('id', 'in', ranking_ids)])
        return {"data": await self.ranking_repository.remove(rankings)}
