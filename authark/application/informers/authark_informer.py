from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, CredentialRepository, DominionRepository,
    RoleRepository)
from ..utilities import QueryDomain, RecordList


class AutharkInformer(ABC):

    @abstractmethod
    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 0,
                     offset: int = 0) -> RecordList:
        """Returns a list of <<model>> dictionaries matching the domain"""

    @abstractmethod
    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        """Returns a the <<model>> records count"""



class StandardAutharkInformer(AutharkInformer):

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository

    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 1000,
                     offset: int = 0) -> RecordList:
        repository = getattr(self, f'{model}_repository')
        return [vars(entity) for entity in
                await repository.search(
                domain or [], limit=limit, offset=offset)]

    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        repository = getattr(self, f'{model}_repository')
        return await repository.count(domain or [])
