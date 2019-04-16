from ....application.models import Dominion
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import DominionRepository
from .json_repository import JsonRepository


class JsonDominionRepository(
        JsonRepository[Dominion], DominionRepository):
    """Json Dominion Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'dominions') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, Dominion)
