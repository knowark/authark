import uuid
from typing import List, Dict
from ...domain.common import (
    TokenString, TokensDict, AuthError, AuthProvider,
    UserCreationError, RecordList, QueryDomain,
    AnonymousUser)
from ...domain.models import Token, User, Tenant, Credential, Dominion
from ...domain.services.repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ...domain.services import (
    RefreshTokenService, HashService, AccessService,
    EnrollmentService, VerificationService, IdentityService)
from ...general import PlanSupplier, TenantSupplier
from ...general.suppliers.plan.events import (
    UserRegistered, PasswordReset)


class ProcedureManager:
    def __init__(
        self, auth_provider: AuthProvider,
        user_repository: UserRepository,
        enrollment_service: EnrollmentService,
        verification_service: VerificationService,
        identity_service: IdentityService,
        plan_supplier: PlanSupplier,
        tenant_supplier: TenantSupplier
    ) -> None:
        self.auth_provider = auth_provider
        self.user_repository = user_repository
        self.enrollment_service = enrollment_service
        self.verification_service = verification_service
        self.identity_service = identity_service
        self.plan_supplier = plan_supplier
        self.tenant_supplier = tenant_supplier
        self.provider_pattern = '@provider.oauth'

    async def register(self, user_dicts: RecordList) -> None:
        registration_tuples = []
        for user_dict in user_dicts:

            tenant_dict = {
                'name': user_dict.pop('organization'),
                'zone': user_dict.pop('zone', ''),
                'email': user_dict['email'],
                'attributes': user_dict.get('attributes', {})
            }
            if not user_dict.get('enroll'):
                self.tenant_supplier.create_tenant(tenant_dict)

            tenant = await self._session_tenant(tenant_dict['name'])

            password = user_dict.pop('password', '')
            username = user_dict.get('username', '')
            if username.endswith(self.provider_pattern):
                provider = username.replace(self.provider_pattern, '')
                user = await self.identity_service.identify(
                    provider, password)
                user.active = False
                credential = Credential(value=uuid.uuid4())
                registration_tuples.append((user, credential))
                continue

            registration_tuples.append((
                User(**user_dict, active=False), Credential(value=password)))

        users = await self.enrollment_service.register(registration_tuples)

        for user in users:
            await self.plan_supplier.notify(UserRegistered(**{
                'type': 'activation',
                'subject': 'Account Activation',
                'recipient': user.email,
                'owner': user.name,
                'token': self.verification_service.generate_token(
                    tenant, user, 'activation').value
            }))

    async def fulfill(self, requisition_dicts: RecordList) -> None:
        reset_records = [
            requisition for requisition in requisition_dicts
            if requisition['type'] == 'reset']

        for record in reset_records:
            tenant = await self._session_tenant(record['tenant'])

            data = record['data']
            [user] = await self.user_repository.search(
                [('email', '=', data['email'])])
            token = self.verification_service.generate_token(
                tenant,    user, 'reset')

            await self.plan_supplier.notify(PasswordReset(**{
                'type': 'reset',
                'subject': 'Password Reset',
                'recipient': user.email,
                'owner': user.name,
                'token': token.value
            }))

    async def verify(self, verification_dicts: RecordList) -> None:
        for record in verification_dicts:
            tenant = await self._session_tenant(record['tenant'])
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

    async def _session_tenant(self, tenant_name: str) -> Tenant:
        tenant_dict = self.tenant_supplier.resolve_tenant(tenant_name)
        tenant = Tenant(**tenant_dict)
        anonymouns_session = AnonymousUser(
            tid=tenant.id, tenant=tenant.slug,
            organization=tenant.name)
        self.auth_provider.setup(anonymouns_session)
        return tenant
