from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from authark.application.utilities.type_definitions import QueryDomain
from authark.application.models.credential import Credential
from authark.application.repositories.expression_parser import ExpressionParser


class CredentialRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> Credential:
        "Get method to be implemented."

    @abstractmethod
    def add(self, credential: Credential) -> bool:
        "Add method to be implemented."

    @abstractmethod
    def search(self, domain: QueryDomain,
               limit: int, offset: int) -> List[Credential]:
        "Search credentials matching a query domain"

    @abstractmethod
    def remove(self, credential: Credential) -> bool:
        "Remove method to be implemented."


class MemoryCredentialRepository(CredentialRepository):
    def __init__(self, parser: ExpressionParser) -> None:
        self.credentials_dict = {}  # type: Dict[str, Credential]
        self.parser = parser

    def get(self, id: str) -> Optional[Credential]:
        user = self.credentials_dict.get(id)
        return user

    def add(self, credential: Credential) -> bool:
        id = credential.id
        self.credentials_dict[id] = credential
        return True

    def search(self, domain: QueryDomain, limit=100, offset=0
               ) -> List[Credential]:
        credentials = []
        filter_function = self.parser.parse(domain)
        for credential in list(self.credentials_dict.values()):
            if filter_function(credential):
                credentials.append(credential)

        if limit:
            credentials = credentials[:limit]
        if offset:
            credentials = credentials[offset:]
        return credentials

    def remove(self, credential: Credential) -> bool:
        if credential.id not in self.credentials_dict:
            return False
        del self.credentials_dict[credential.id]
        return True

    def load(self, credentials_dict: Dict[str, Credential]) -> None:
        self.credentials_dict = credentials_dict
