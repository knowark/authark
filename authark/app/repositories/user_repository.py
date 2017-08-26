from abc import ABC, abstractmethod
from authark.app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, uid: str) -> User:
        ...

    @abstractmethod
    def save(self, user: User) -> bool:
        ...
