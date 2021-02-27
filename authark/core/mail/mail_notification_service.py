from typing import Dict, Any
from email.message import EmailMessage
from aiosmtplib import send
from ...application.domain.common import NotificationError
from ...application.domain.services import NotificationService



class MailNotificationService(NotificationService):
    def __init__(self, sender: str, host: str, port: int,
                 username: str, password: str) -> None:
        self.sender = sender
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def notify(self, notification: Dict[str, Any]) -> None:
        await super().notify(notification)

        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = notification['recipient']
        message['Subject'] = notification['subject']

        message.set_content(
            f"{notification['owner']} + {notification['token']}")

        await send(message, hostname=self.host, port=self.port,
                   username=self.username, password=self.password,
                   use_tls=True)
