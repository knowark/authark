from ..application.domain.services import NotificationService
from ..core.common import Config
from ..core.mail import MailNotificationService
from .json_factory import JsonFactory


class WebFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.mail_config = self.config.get('mail', {})

    # Services

    def notification_service(self) -> NotificationService:
        return MailNotificationService(
            self.mail_config['sender'],
            self.mail_config['host'],
            self.mail_config['port'],
            self.mail_config['username'],
            self.mail_config['password'])

