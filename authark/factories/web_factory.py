from ..application.domain.services import NotificationService
from ..core.suppliers import TemplateSupplier
from ..core.common import Config
from ..core.mail import MailNotificationService
from .json_factory import JsonFactory


class WebFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.mail_config = self.config.get('mail', {})

    # Services

    def notification_service(
        self, template_supplier: TemplateSupplier) -> NotificationService:
        return MailNotificationService(
            self.mail_config, template_supplier)
