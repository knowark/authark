from typing import Dict
from authark.app.models.user import User
from authark.app.repositories.user_repository import UserRepository


class MemoryUserRepository(UserRepository):

    def __init__(self) -> None:
        self.user_dict = {}  # type: Dict[str, User]

    def get(self, uid: str) -> User:
        user = self.user_dict.get(uid)
        return user

    def save(self, user: User) -> bool:
        uid = user.uid
        self.user_dict[uid] = user
        return True

    def load(self, user_dict: Dict[str, User]) -> None:
        self.user_dict = user_dict
