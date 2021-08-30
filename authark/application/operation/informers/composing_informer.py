from abc import ABC, abstractmethod
from ...domain.repositories import (
    DominionRepository, RoleRepository, RankingRepository)
from ...domain.common import ExtendedRankingDictList


class ComposingInformer(ABC):

    @abstractmethod
    async def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        """List user roles, resolving model references"""


class StandardComposingInformer(ComposingInformer):

    def __init__(self, dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        rankings = await self.ranking_repository.search(
            [('user_id', '=', user_id)])

        roles = {role.id: role for role in await self.role_repository.search(
            [('id', 'in', [ranking.role_id for ranking in rankings])])}

        dominions = {dominion.id: dominion for dominion in
                     await self.dominion_repository.search(
                         [('id', 'in', [role.dominion_id for role in
                                        roles.values()])])}

        result = []
        for ranking in rankings:
            role = roles[ranking.role_id]
            dominion = dominions[role.dominion_id]
            result.append({'ranking_id': ranking.id, 'role': role.name,
                           'dominion': dominion.name})

        return result
