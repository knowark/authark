from ....application.models import Role
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import RoleRepository
from .json_repository import JsonRepository


class JsonRoleRepository(
        JsonRepository[Role], RoleRepository):
    """Json Role Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'roles') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, Role)
