from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from ..utilities import QueryDomain, ExtendedRankingDictList


class ComposingInformer(ABC):

    @abstractmethod
    async def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        """List user roles, resolving model references"""


class StandardComposingInformer(ComposingInformer):

    def __init__(self,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository
                 ) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    async def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        rankings = await self.ranking_repository.search(
            [('user_id', '=', user_id)])
        for ranking in rankings:
            role = await self.role_repository.search(
                [('id', '=', ranking.role_id)])
            dominion = await self.dominion_repository.search(
                [('id', '=', role[0].dominion_id)])
            print("dominion en comsposing   ",dominion[0].name)
            
            result = []    
            result.append({'ranking_id': ranking.id, 'role': role[0].name,
                           'dominion': dominion[0].name})
        return result

        # duda role y dominion cambian get por search
