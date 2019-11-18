from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, CredentialRepository, DominionRepository,
    RoleRepository, ResourceRepository)
from .types import (
    QueryDomain, UserDictList, CredentialDictList,
    DominionDictList, RoleDictList, ResultDictList)


class AutharkReporter(ABC):

    @abstractmethod
    def search_users(self, domain: QueryDomain) -> UserDictList:
        """Search Authark's users"""

    @abstractmethod
    def search_credentials(self, domain: QueryDomain) -> CredentialDictList:
        """Search Authark's credentials"""

    @abstractmethod
    def search_dominions(self, domain: QueryDomain) -> DominionDictList:
        """Search Authark's dominions"""

    @abstractmethod
    def search_roles(self, domain: QueryDomain) -> RoleDictList:
        """Search Authark's roles"""



    @abstractmethod
    def search_resources(self, domain: QueryDomain) -> ResultDictList:
        """Search Authark's resources"""


class StandardAutharkReporter(AutharkReporter):

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 resource_repository: ResourceRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.resource_repository = resource_repository

    def search_users(self, domain: QueryDomain) -> UserDictList:
        return [vars(user) for user in sorted(
            self.user_repository.search(domain),
            key=lambda x: x.username)]

    def search_credentials(self, domain: QueryDomain) -> CredentialDictList:
        return [vars(credential) for credential in
                self.credential_repository.search(domain)]

    def search_dominions(self, domain: QueryDomain) -> DominionDictList:
        return [vars(dominion) for dominion in
                sorted(self.dominion_repository.search(domain),
                       key=lambda x: x.name)]

    def search_roles(self, domain: QueryDomain) -> RoleDictList:
        return [vars(role) for role in
                sorted(self.role_repository.search(domain),
                       key=lambda x: x.name)]

    def search_resources(self, domain: QueryDomain) -> RoleDictList:
        return [vars(resource) for resource in
                sorted(self.resource_repository.search(domain),
                       key=lambda x: x.name)]
