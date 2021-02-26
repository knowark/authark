from typing import Dict, Any
from email.message import EmailMessage
from aiosmtplib import send
from ...application.domain.services import NotificationService



class MailNotificationService(NotificationService):
    def __init__(self, sender: str, host: str, port: int,
                 username: str, password: str) -> None:
        self.sender = sender
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def notify(self, content: Dict[str, Any]) -> None:
        self.content = content

        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = content['recipient']
        message['Subject'] = content['subject']
        message.set_content(content['body'])

        await send(message, hostname=self.host, port=self.port,
                   username=self.username, password=self.password)

