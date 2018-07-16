from abc import ABC, abstractmethod
from typing import Dict, Optional
from authark.application.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, username: str) -> User:
        "Get method to be implemented."

    def save(self, user: User) -> bool:
        existing_user = self.get(user.username)
        if existing_user and existing_user.username:
            return False

        return self.save_(user)

    @abstractmethod
    def save_(self, user: User) -> bool:
        "Internal save method to be implemented."


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.user_dict = {}  # type: Dict[str, User]

    def get(self, username: str) -> Optional[User]:
        user = self.user_dict.get(username)
        return user

    def save_(self, user: User) -> bool:
        username = user.username
        self.user_dict[username] = user
        return True

    def load(self, user_dict: Dict[str, User]) -> None:
        self.user_dict = user_dict
