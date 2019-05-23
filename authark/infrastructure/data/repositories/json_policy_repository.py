from ....application.models import Policy
from ....application.services import TenantProvider
from ....application.utilities import ExpressionParser
from ....application.repositories import PolicyRepository
from .json_repository import JsonRepository


class JsonPolicyRepository(
        JsonRepository[Policy], PolicyRepository):
    """Json Policy Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'policies') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, Policy)
