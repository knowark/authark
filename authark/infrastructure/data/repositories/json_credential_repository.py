from ....application.models import Credential
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import CredentialRepository
from .json_repository import JsonRepository


class JsonCredentialRepository(
        JsonRepository[Credential], CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'credentials') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, Credential)
