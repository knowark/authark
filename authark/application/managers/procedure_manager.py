from typing import List, Dict
from ..domain.common import (
    TokenString, TokensDict, AuthError,
    UserCreationError, RecordList, QueryDomain)
from ..domain.models import Token, User, Credential, Dominion
from ..domain.repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ..domain.services import (
    RefreshTokenService, HashService, AccessService,
    VerificationService, NotificationService)


class ProcedureManager:
    def __init__(
        self, user_repository: UserRepository,
        verification_service: VerificationService,
        notification_service: NotificationService
    ) -> None:
        self.user_repository = user_repository
        self.verification_service = verification_service
        self.notification_service = notification_service

    async def fulfill(self, requisition_dicts: RecordList) -> None:
        reset_records = [
            requisition for requisition in requisition_dicts
            if requisition['type'] == 'reset']

        for record in reset_records:
            data = record['data']
            [user] = await self.user_repository.search(
                [('email', '=', data['email'])])
            token = self.verification_service.generate_token(user, 'reset')

            await self.notification_service.notify({
                'type': 'reset',
                'subject': 'Password Reset',
                'recipient': user.email,
                'owner': user.name,
                'token': token.value
            })
