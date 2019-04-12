from ....application.models import Ranking
from ....application.utilities import ExpressionParser
from ....application.repositories import RankingRepository
from .json_repository import JsonRepository


class JsonRankingRepository(
        JsonRepository[Ranking], RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'rankings') -> None:
        super().__init__(file_path, parser, collection_name, Ranking)
