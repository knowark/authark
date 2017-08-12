from abc import ABC, abstractmethod


class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class UserContainer(ABC):
    @abstractmethod
    def get(self, uid: str) -> User:
        ...
