from ..application.domain.services import NotificationService
from ..core.suppliers import TemplateSupplier, JinjaTemplateSupplier
from ..core.common import Config
from ..core.mail import HttpNotificationService
from .json_factory import JsonFactory


class WebFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.mail_config = self.config.get('mail', {})
        self.verification_config = self.config.get('verification', {})

    # Services

    def template_supplier(self) -> TemplateSupplier:
        templates = self.config.get('templates', [])
        return JinjaTemplateSupplier(templates)

    def notification_service(
        self, template_supplier: TemplateSupplier) -> NotificationService:
        config = self.config['notification']
        return HttpNotificationService(config)
