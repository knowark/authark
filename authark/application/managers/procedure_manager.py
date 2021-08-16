from typing import List, Dict
from ..domain.common import (
    TokenString, TokensDict, AuthError,
    UserCreationError, RecordList, QueryDomain)
from ..domain.models import Token, User, Credential, Dominion
from ..domain.repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ..domain.services import (
    RefreshTokenService, HashService, AccessService,
    EnrollmentService, VerificationService, NotificationService)
from ..general import Planner


class ProcedureManager:
    def __init__(
        self, user_repository: UserRepository,
        enrollment_service: EnrollmentService,
        verification_service: VerificationService,
        notification_service: NotificationService,
        planner: Planner
    ) -> None:
        self.user_repository = user_repository
        self.enrollment_service = enrollment_service
        self.verification_service = verification_service
        self.notification_service = notification_service
        self.planner = planner

    async def register(self, user_dicts: RecordList) -> None:
        registration_tuples = []
        for user_dict in user_dicts:
            password = user_dict.pop('password', '')
            registration_tuples.append((
                User(**user_dict, active=False), Credential(value=password)))

        users = await self.enrollment_service.register(registration_tuples)

        for user in users:
            await self.notification_service.notify({
                'type': 'activation',
                'subject': 'Account Activation',
                'recipient': user.email,
                'owner': user.name,
                'token': self.verification_service.generate_token(
                    user, 'activation').value
            })

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

    async def verify(self, verification_dicts: RecordList) -> None:
        for record in verification_dicts:
            token_dict = await self.verification_service.verify(dict(record))
            [user] = await self.user_repository.search(
                [('id', '=', token_dict['uid'])])
            if token_dict['type'] == 'activation':
                user.active = True
                await self.user_repository.add(user)
            else:
                credential = Credential(value=record['data']['password'])
                await self.enrollment_service.set_credentials(
                    [user], [credential])

    async def update(self, user_dicts: RecordList) -> None:
        credentials = [Credential(value=user_dict.pop('password', ''))
                       for user_dict in user_dicts]
        users = ([User(**user_dict) for user_dict in user_dicts])

        users = await self.user_repository.add(users)
        await self.enrollment_service.set_credentials(users, credentials)

    async def deregister(self, user_ids: List[str]) -> bool:
        users = await self.user_repository.search([('id', 'in', user_ids)])
        return await self.enrollment_service.deregister(users)
