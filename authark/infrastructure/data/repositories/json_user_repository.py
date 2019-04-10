from authark.application.models.user import User
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.repositories.user_repository import UserRepository
from authark.infrastructure.data.json_repository import JsonRepository


class JsonUserRepository(JsonRepository[User], UserRepository):
    """Json User Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'users') -> None:
        super().__init__(file_path, parser, collection_name, User)
