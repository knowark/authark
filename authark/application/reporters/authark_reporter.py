from abc import ABC, abstractmethod
from authark.application.utilities.type_definitions import QueryDomain
from authark.application.repositories.user_repository import UserRepository


class AutharkReporter(ABC):

    @abstractmethod
    def search_users(self, domain: QueryDomain):
        """Search Authark's users"""


class MemoryAutharkReporter(AutharkReporter):

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def search_users(self, domain: QueryDomain):
        return self.user_repository.search(domain)
