from ....application.models import Grant
from ....application.services import TenantProvider
from ....application.utilities import ExpressionParser
from ....application.repositories import GrantRepository
from .json_repository import JsonRepository


class JsonGrantRepository(
        JsonRepository[Grant], GrantRepository):
    """Json Grant Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'grants') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, Grant)
