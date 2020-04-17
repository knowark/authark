from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository)
from ..utilities import QueryDomain, RecordList


class ComposingInformer(ABC):

    @abstractmethod
    async def list_user_roles(self,
                              user_id: str,
                              domain: QueryDomain = None,
                              limit: int = 0,
                              offset: int = 0
                              ) -> RecordList:
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

    async def list_user_roles(self,
                              user_id: str,
                              domain: QueryDomain = None,
                              limit: int = 0,
                              offset: int = 0
                              ) -> RecordList:
        rankings = await self.ranking_repository.search(
            [('user_id', '=', user_id)])
        result = []
        for ranking in rankings:
            # role = await self.role_repository.search(
            #     ranking.role_id
            # )
            role = await self.role_repository.search(
                domain or [], limit=limit, offset=offsetd
            )
            dominion = await self.dominion_repository.search(role.dominion_id)
            result.append({'ranking_id': ranking.id, 'role': role.name,
                           'dominion': dominion.name})

        return result
