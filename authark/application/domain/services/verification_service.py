from typing import Dict, Any, List
from ..models import User, Token, Dominion
from ..repositories import UserRepository
from ..common import TenantProvider, Tenant
from .token_service import VerificationTokenService


class VerificationService:

    def __init__(self, user_repository: UserRepository,
                 token_service: VerificationTokenService,
                 tenant_provider: TenantProvider) -> None:
        self.user_repository = user_repository
        self.token_service = token_service
        self.tenant_provider = tenant_provider

    def generate_token(self, user: User) -> Token:
        tenant = self.tenant_provider.tenant
        verification_token = self.token_service.generate_token(
            {'type': 'activation', 'tenant': tenant.slug, 'user_id': user.id})
        return verification_token

    async def verify(self, verification_dict: Dict[str, Any]) -> None:
        tenant = verification_dict['tenant']
        token = Token(verification_dict['token'])

        token_dict = self.token_service.decode(token)

        [user] = await self.user_repository.search(
            [('id', '=', token_dict['user_id'])])
        user.active = True
        await self.user_repository.add(user)