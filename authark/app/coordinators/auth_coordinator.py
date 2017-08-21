from abc import ABC, abstractmethod


class AuthCoordinator(ABC):

    @abstractmethod
    def authenticate(self, uid: str) -> None:
        ...
