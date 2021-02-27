from typing import Dict, Any
from abc import ABC, abstractmethod
from ..common import NotificationError
from ..models import Token


class NotificationService(ABC):

    types = {'activation'}

    @abstractmethod
    async def notify(self, notification: Dict[str, Any]) -> None:
        "Notify method to be implemented."
        if notification['type'] not in self.types:
            raise NotificationError(
                f'The notification type must be one of: {self.types}')


class MemoryNotificationService(NotificationService):
    def __init__(self) -> None:
        self.notification: Dict[str, Any] = {}

    async def notify(self, notification: Dict[str, Any]) -> None:
        await super().notify(notification)
        self.notification = notification
