from typing import Dict, Any, List
from ..models import User, Tenant, Token, Dominion
from .repositories import UserRepository
from .token_service import VerificationTokenService


class VerificationService:
    def __init__(self, user_repository: UserRepository,
                 token_service: VerificationTokenService) -> None:
        self.user_repository = user_repository
        self.token_service = token_service

    def generate_token(self, tenant: Tenant, user: User, type: str) -> Token:
        verification_token = self.token_service.generate_token({
            'type': type, 'tenant': tenant.slug,
            'tid': tenant.id, 'uid': user.id,'temail': tenant.email})
        return verification_token

    def generate_token_tenant(self, tenant: Tenant, type: str) -> Token:
        verification_token = self.token_service.generate_token({
            'type': type, 'tenant': tenant.slug,
            'tid': tenant.id, 'temail': tenant.email})
        return verification_token

    def generate_authorization(self, tenant: Tenant, user: User) -> Token:
        authorization_token = self.token_service.generate_token({
            'type': 'authorization', 'tenant': tenant.slug,
            'tid': tenant.id, 'uid': user.id,
            'name': user.name, 'email': user.email})
        return authorization_token

    async def verify(
        self, verification_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        tenant = verification_dict['tenant']
        token = Token(verification_dict['token'])

        return self.token_service.decode(token)
