from ....application.models import Role
from ....application.repositories import (
    ExpressionParser, RoleRepository)
from .json_repository import JsonRepository


class JsonRoleRepository(
        JsonRepository[Role], RoleRepository):
    """Json Role Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'roles') -> None:
        super().__init__(file_path, parser, collection_name, Role)
