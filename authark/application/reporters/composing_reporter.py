from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    ResourceRepository)
from .types import (
    QueryDomain, UserDictList, DominionDictList, RoleDictList,
    ExtendedRankingDictList, ExtendedDictList)


class ComposingReporter(ABC):

    @abstractmethod
    def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        """List user roles, resolving model references"""


class StandardComposingReporter(ComposingReporter):

    def __init__(self,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 resource_repository: ResourceRepository
                 ) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.resource_repository = resource_repository

    def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        rankings = self.ranking_repository.search(
            [('user_id', '=', user_id)])
        result = []
        for ranking in rankings:
            role = self.role_repository.get(ranking.role_id)
            dominion = self.dominion_repository.get(role.dominion_id)
            result.append({'ranking_id': ranking.id, 'role': role.name,
                           'dominion': dominion.name})

        return result
