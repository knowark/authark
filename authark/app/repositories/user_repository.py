from abc import ABC, abstractmethod
from authark.app.models.user import User


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
