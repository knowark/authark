from abc import ABC, abstractmethod
from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.application.utilities.type_definitions import (
    QueryDomain, UserDictList, CredentialDictList)


class AutharkReporter(ABC):

    @abstractmethod
    def search_users(self, domain: QueryDomain) -> UserDictList:
        """Search Authark's users"""

    @abstractmethod
    def search_credentials(self, domain: QueryDomain) -> CredentialDictList:
        """Search Authark's credentials"""


class MemoryAutharkReporter(AutharkReporter):

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository

    def search_users(self, domain: QueryDomain) -> UserDictList:
        return [vars(user) for user in self.user_repository.search(domain)]

    def search_credentials(self, domain: QueryDomain) -> CredentialDictList:
        return [vars(credential) for credential in
                self.credential_repository.search(domain)]
