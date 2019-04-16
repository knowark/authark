from ....application.models import Permission
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import PermissionRepository
from .json_repository import JsonRepository


class JsonPermissionRepository(
        JsonRepository[Permission], PermissionRepository):
    """Json Permission Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'permissions') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, Permission)
