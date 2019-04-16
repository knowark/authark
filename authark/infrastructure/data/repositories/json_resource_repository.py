from ....application.models import Resource
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import ResourceRepository
from .json_repository import JsonRepository


class JsonResourceRepository(
        JsonRepository[Resource], ResourceRepository):
    """Json Resource Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'resources') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, Resource)
