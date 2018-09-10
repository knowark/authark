from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.infrastructure.data.json_repository import JsonRepository


class JsonUserRepository(JsonRepository[User], UserRepository):
    """Json User Repository"""
