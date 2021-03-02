from typing import Dict, Any
from email.message import EmailMessage
from aiosmtplib import send
from ...application.domain.common import NotificationError
from ...application.domain.services import NotificationService
from ..suppliers import TemplateSupplier


class MailNotificationService(NotificationService):
    def __init__(self, config: Dict[str, Any],
                 template_supplier: TemplateSupplier) -> None:
        self.sender = config['sender']
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.url = config['url']
        self.template_supplier = template_supplier

    async def notify(self, notification: Dict[str, Any]) -> None:
        await super().notify(notification)

        context = {'url': self.url, **notification}
        content = self.template_supplier.render('activation.html', context)

        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = notification['recipient']
        message['Subject'] = notification['subject']
        message.add_header('Content-Type', 'text/html')
        message.set_payload(content)

        await send(message, hostname=self.host, port=self.port,
                   username=self.username, password=self.password,
                   use_tls=True)
