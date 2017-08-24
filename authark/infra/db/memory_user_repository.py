from typing import List
from authark.app.models.user import User
from authark.app.repositories.user_repository import UserRepository


class MemoryUserRepository(UserRepository):

    def __init__(self) -> None:
        self.user_list = []  # type: List[User]

    def get(self, uid: str) -> User:
        user = User(name='Esteban', email='Echeverry')
        return user

    def load(self, user_list: List[User]) -> None:
        self.user_list = user_list
