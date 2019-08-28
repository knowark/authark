from ....application.models import User
from ....application.utilities import ExpressionParser, TenantProvider
from ....application.repositories import UserRepository
from .json_repository import JsonRepository


class JsonUserRepository(JsonRepository[User], UserRepository):
    """Json User Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'users') -> None:
        super().__init__(file_path, parser, tenant_provider,
                         collection_name, User)
