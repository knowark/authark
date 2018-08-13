from abc import ABC, abstractmethod
from authark.application.utilities.type_definitions import (
    QueryDomain, UserDictList)
from authark.application.reporters.authark_reporter import AutharkReporter
from authark.infrastructure.data.json_user_repository import JsonUserRepository


class JsonAutharkReporter(AutharkReporter):

    def __init__(self, user_repository: JsonUserRepository) -> None:
        self.user_repository = user_repository

    def search_users(self, domain: QueryDomain) -> UserDictList:
        import logging
        logger = logging.getLogger()
        data = self.user_repository.search(domain)
        logger.debug("DATA ~~~~||| =======>>> %s", data)
        return [vars(user) for user in self.user_repository.search(domain)]
