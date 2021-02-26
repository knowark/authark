from typing import Dict, Any
from abc import ABC, abstractmethod
from ..models import Token


class NotificationService(ABC):
    @abstractmethod
    async def notify(self, content: Dict[str, Any]) -> None:
        "Notify method to be implemented."


class MemoryNotificationService(NotificationService):
    def __init__(self) -> None:
        self.content: Dict[str, Any] = {}

    async def notify(self, content: Dict[str, Any]) -> None:
        self.content = content

