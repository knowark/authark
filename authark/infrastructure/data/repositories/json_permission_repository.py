from ....application.models import Permission
from ....application.utilities import ExpressionParser
from ....application.repositories import PermissionRepository
from .json_repository import JsonRepository


class JsonPermissionRepository(
        JsonRepository[Permission], PermissionRepository):
    """Json Permission Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'permissions') -> None:
        super().__init__(file_path, parser, collection_name, Permission)
