from ...application.models import Resource
from ...application.repositories import (
    ExpressionParser, ResourceRepository)
from .json_repository import JsonRepository


class JsonResourceRepository(
        JsonRepository[Resource], ResourceRepository):
    """Json Resource Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'resources') -> None:
        super().__init__(file_path, parser, collection_name, Resource)
