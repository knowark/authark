from ...application.domain.services import IdentityService
from ..core.oauth import OauthIdentityService
from .web_factory import WebFactory


class OauthFactory(WebFactory):
    def identity_service(self) -> IdentityService:
        return OauthIdentityService(self.config['oauth'])

