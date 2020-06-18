from abc import ABC, abstractmethod
from typing import Union, List, Tuple, overload
from ..domain.repositories import (
    UserRepository, CredentialRepository,
    DominionRepository, RoleRepository,
    RuleRepository, PolicyRepository, RankingRepository)
from ..domain.common import QueryDomain, DataDict, RecordList


class AutharkInformer(ABC):

    @abstractmethod
    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        """Returns a the <<model>> records count"""

    @overload
    async def search(self, model: str, domain: QueryDomain,
                     limit: int = None, offset: int = None) -> RecordList:
        """Standard search method"""

    @overload
    async def search(
            self, model: str, domain: QueryDomain,
            limit: int = None, offset: int = None,
            *,
            join: str, link: str = None,
            source: str = None, target: str = None) -> List[
                Tuple[DataDict, RecordList]]:
        """Joining search method"""

    @abstractmethod
    async def search(
            self, model: str, domain: QueryDomain = None,
            limit: int = None, offset: int = None,
            *,
            join: str = None, link: str = None,
            source: str = None, target: str = None) -> Union[
                RecordList, List[Tuple[DataDict, RecordList]]]:
        """Returns a list of <<model>> dictionaries matching the domain"""


class StandardAutharkInformer(AutharkInformer):
    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 rule_repository: RuleRepository,
                 policy_repository: PolicyRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.rule_repository = rule_repository
        self.policy_repository = policy_repository
        self.ranking_repository = ranking_repository

    async def count(self,
                    collection: str,
                    domain: QueryDomain = None) -> int:
        repository = getattr(self, f'{collection}_repository')
        return await repository.count(domain or [])

    @overload
    async def search(self,  model: str, domain: QueryDomain,
                     limit: int = None, offset: int = None) -> RecordList:
        """Standard search method"""

    @overload
    async def search(
            self, model: str, domain: QueryDomain,
            limit: int = None, offset: int = None,
            *,
            join: str, link: str = None,
            source: str = None, target: str = None) -> List[
                Tuple[DataDict, RecordList]]:
        """Joining search method"""

    async def search(
            self, model: str, domain: QueryDomain = None,
            limit: int = None, offset: int = None,
            *,
            join: str = None, link: str = None,
            source: str = None, target: str = None) -> Union[
                RecordList, List[Tuple[DataDict, RecordList]]]:

        repository = getattr(self, f'{model}_repository')
        reference = getattr(self, f'{join}_repository', None)
        pivot = getattr(self, f'{link}_repository', None)

        items = await repository.search(
            domain or [], limit=limit, offset=offset,
            join=reference, link=pivot, source=source, target=target)

        result = []
        for item in items:
            if not isinstance(item, (tuple, list)):
                result.append(item)
                continue
            result.append((vars(item[0]), [vars(i) for i in item[1]]))

        return result
