from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Any, overload
from ...domain.services.repositories import (
    UserRepository, CredentialRepository,
    DominionRepository, RoleRepository,
    RestrictionRepository, PolicyRepository, RankingRepository)
from ...domain.common import QueryDomain, DataDict, RecordList


class AutharkInformer(ABC):

    @abstractmethod
    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        """Standard count method"""

    @abstractmethod
    async def search(self, model: str, domain: QueryDomain,
                     limit: int = None, offset: int = None,
                     order: str = None) -> RecordList:
        """Standard search method"""

    @abstractmethod
    async def join(self, model: str, domain: QueryDomain,
                   join: str = None, link: str = None,
                   source: str = None, target: str = None
                   ) -> List[Tuple[DataDict, RecordList]]:
        """Standard join method"""


class StandardAutharkInformer(AutharkInformer):
    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 restriction_repository: RestrictionRepository,
                 policy_repository: PolicyRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.restriction_repository = restriction_repository
        self.policy_repository = policy_repository
        self.ranking_repository = ranking_repository

    async def count(self,
                    collection: str,
                    domain: QueryDomain = None) -> int:
        repository = getattr(self, f'{collection}_repository')
        return await repository.count(domain or [])

    async def search(self,  model: str, domain: QueryDomain = None,
                     limit: int = None, offset: int = None,
                     order: str = None) -> RecordList:
        """Standard search method"""

        repository = getattr(self, f'{model}_repository')

        items = await repository.search(
            domain or [], limit=limit, offset=offset, order=order)

        return [vars(item) for item in items]

    async def join(self, model: str, domain: QueryDomain = None,
                   join: str = None, link: str = None,
                   source: str = None, target: str = None
                   ) -> List[Tuple[DataDict, RecordList]]:

        repository = getattr(self, f'{model}_repository')
        reference = getattr(self, f'{join}_repository', None)
        pivot = getattr(self, f'{link}_repository', None)

        items = await repository.join(
            domain or [], join=reference, link=pivot,
            source=source, target=target)

        return [(vars(item[0]), [vars(i) for i in item[1]])
                for item in items]
