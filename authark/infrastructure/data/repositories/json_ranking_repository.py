from ....application.models import Ranking
from ....application.utilities import ExpressionParser, TenantProvider
from ....application.repositories import RankingRepository
from .json_repository import JsonRepository


class JsonRankingRepository(JsonRepository[Ranking], RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'rankings') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, Ranking)
