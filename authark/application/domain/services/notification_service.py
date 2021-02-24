import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..models import Token


class NotificationService(ABC):
    @abstractmethod
    def notify(self, content: Dict[str, Any]) -> None:
        "Notify method to be implemented."


class MemoryNotificationService(NotificationService):
    def __init__(self) -> None:
        self.content: Dict[str, Any] = {}

    def notify(self, content: Dict[str, Any]) -> None:
        self.content = content

