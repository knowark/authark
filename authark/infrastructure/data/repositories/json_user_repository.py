from ....application.models import User
from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import UserRepository
from .json_repository import JsonRepository


class JsonUserRepository(JsonRepository[User], UserRepository):
    """Json User Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str = 'users') -> None:
        super().__init__(file_path, parser, tenant_service,
                         collection_name, User)
