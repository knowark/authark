from ....application.models import Resource
from ....application.services import TenantProvider
from ....application.utilities import ExpressionParser
from ....application.repositories import ResourceRepository
from .json_repository import JsonRepository


class JsonResourceRepository(
        JsonRepository[Resource], ResourceRepository):
    """Json Resource Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'resources') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, Resource)
