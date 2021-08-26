from typing import Dict, Any, List
from ..models import User, Tenant, Token, Dominion
from ..repositories import UserRepository
from .token_service import VerificationTokenService


class VerificationService:
    def __init__(self, user_repository: UserRepository,
                 token_service: VerificationTokenService) -> None:
        self.user_repository = user_repository
        self.token_service = token_service

    def generate_token(self, tenant: Tenant, user: User, type: str) -> Token:
        verification_token = self.token_service.generate_token({
            'type': type, 'tenant': tenant.slug,
            'tid': tenant.id, 'uid': user.id})
        return verification_token

    async def verify(
        self, verification_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        tenant = verification_dict['tenant']
        token = Token(verification_dict['token'])

        return self.token_service.decode(token)
