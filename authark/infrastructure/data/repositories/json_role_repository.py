from ....application.models import Role
from ....application.utilities import QueryParser, TenantProvider
from ....application.repositories import RoleRepository
from .json_repository import JsonRepository


class JsonRoleRepository(JsonRepository[Role], RoleRepository):
    """Json Role Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'roles') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, Role)
