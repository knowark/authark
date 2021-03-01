from typing import Dict, Any, List
from ..models import User, Token, Dominion
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository)
from ..common import TenantProvider, Tenant
from .token_service import VerificationTokenService


class VerificationService:

    def __init__(self, token_service: VerificationTokenService,
                 tenant_provider: TenantProvider) -> None:
        self.token_service = token_service
        self.tenant_provider = tenant_provider

    def generate_token(self, user: User) -> Token:
        tenant = self.tenant_provider.tenant
        verification_token = self.token_service.generate_token(
            {'type': 'activation', 'tenant': tenant.slug, 'user_id': user.id})
        return verification_token

