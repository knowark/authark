from abc import ABC, abstractmethod
from authark.application.utilities.type_definitions import (
    QueryDomain, UserDictList, CredentialDictList)
from authark.application.reporters.authark_reporter import AutharkReporter
from authark.infrastructure.data.json_user_repository import JsonUserRepository
from authark.infrastructure.data.json_credential_repository import (
    JsonCredentialRepository)


class JsonAutharkReporter(AutharkReporter):

    def __init__(self, user_repository: JsonUserRepository,
                 credential_repository: JsonCredentialRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository

    def search_users(self, domain: QueryDomain) -> UserDictList:
        data = self.user_repository.search(domain)
        return [vars(user) for user in self.user_repository.search(domain)]

    def search_credentials(self, domain: QueryDomain) -> CredentialDictList:
        data = self.credential_repository.search(domain)
        return [vars(credential) for credential in
                self.credential_repository.search(domain)]
