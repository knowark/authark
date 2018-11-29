from ....application.repositories import ExpressionParser
from ...config import Config
from ..data import (
    init_json_database, JsonCredentialRepository,
    JsonDominionRepository, JsonRoleRepository,
    JsonRepository, JsonUserRepository,
    JsonRankingRepository)
from .crypto_factory import CryptoFactory


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.path = config['database']['url']

    # Repositories

    def json_user_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonUserRepository:
        return JsonUserRepository(self.path, expression_parser)

    def json_credential_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonCredentialRepository:
        return JsonCredentialRepository(self.path, expression_parser)

    def json_dominion_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonDominionRepository:
        return JsonDominionRepository(self.path, expression_parser)

    def json_role_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonRoleRepository:
        return JsonRoleRepository(self.path, expression_parser)

    def json_ranking_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonRankingRepository:
        return JsonRankingRepository(self.path, expression_parser)
