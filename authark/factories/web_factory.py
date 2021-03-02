from ..application.domain.services import NotificationService
from ..core.suppliers import TemplateSupplier, JinjaTemplateSupplier
from ..core.common import Config
from ..core.mail import MailNotificationService
from .json_factory import JsonFactory


class WebFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.site_config = self.config.get('site', {})
        self.mail_config = self.config.get('mail', {})

    # Services

    def notification_service(
        self, template_supplier: TemplateSupplier) -> NotificationService:
        config = {**self.site_config, **self.mail_config}
        return MailNotificationService(config, template_supplier)

    def template_supplier(self) -> TemplateSupplier:
        templates = self.config.get('templates', [])
        return JinjaTemplateSupplier(templates)
