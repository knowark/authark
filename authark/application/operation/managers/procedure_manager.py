import uuid
from typing import List, Dict
from ...domain.common import (
    TokenString, TokensDict, AuthError, AuthProvider,
    UserCreationError, RecordList, QueryDomain,
    AnonymousUser, EmailExistsError)
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
        tenant_supplier: TenantSupplier,
        config: dict,
        access_service: AccessService,
        dominion_repository: DominionRepository,
        refresh_token_service: RefreshTokenService,
        credential_repository: CredentialRepository,
        hash_service: HashService,
    ) -> None:
        self.auth_provider = auth_provider
        self.user_repository = user_repository
        self.enrollment_service = enrollment_service
        self.verification_service = verification_service
        self.identity_service = identity_service
        self.plan_supplier = plan_supplier
        self.tenant_supplier = tenant_supplier
        self.provider_pattern = '@provider.oauth'
        self.config = config
        self.access_service = access_service
        self.dominion_repository = dominion_repository
        self.refresh_token_service = refresh_token_service
        self.credential_repository = credential_repository
        self.hash_service = hash_service

    async def register(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        user_dicts = data
        registration_tuples = []
        dominion_name = data.get('dominion', '')
        client = data.get('client', '')
        username = data.get('email')

        tenant_dict = {
            'name': data.pop('organization'),
            'zone': data.pop('zone', ''),
            'email': data['email'],
            'attributes': data.get('attributes', {})
        }
        if not data.get('enroll'):
            self.tenant_supplier.create_tenant(tenant_dict)

        tenant = await self._session_tenant(tenant_dict['name'])

        password = data.pop('password', '')
        email = data.get('email', '')
        if email.endswith(self.provider_pattern):
            provider = email.replace(self.provider_pattern, '')
            user = await self.identity_service.identify(
                provider, password)
            user.active = False
            credential = Credential(value=password)
            registration_tuples.append((user, credential))

        registration_tuples.append((
            User(**data, active=False), Credential(value=password)))

        users = await self.enrollment_service.register(registration_tuples)
        # dominion = await self._ensure_dominion(dominion_name)

        # Create new refresh token
        client = client or 'ALL'

        for user in users:
            await self.plan_supplier.notify(UserRegistered(**{
                'type': 'activation',
                'subject': 'Account Activation',
                'template': 'mail/auth/email_verification.html',
                'recipient': user.email,
                'owner': user.name,
                'authorization': (
                    self.verification_service.generate_authorization(
                    tenant, user).value),
                'context':{
                    'user_name': user.name,
                    'email_link': self.config['email_link'],
                    'unsubscribe_link': self.config['unsubscribe_link'],
                    'verify_link': (self.config['url']+
                                    "/login?verification_token="+
                                    self.verification_service.generate_token(
                                        tenant, user, 'activation').value)
                }
            }))

            # access_token = await self.access_service.generate_token(
                 # tenant, user, dominion)

            # # Create new refresh token
            # refresh_token_str = await self._generate_refresh_token(
                # user.id, client)

        # return {'data': {
                # 'refresh_token': refresh_token_str,
                # 'access_token': access_token.value
        # }}

        if username.endswith(self.provider_pattern):
            return {"data": await self._provider_authenticate(
                username, password, client, dominion_name, tenant.name)}
        return {"data": await self._password_authenticate(
                username, password, client, dominion_name, tenant.name)}

    async def fulfill(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        requisition_dicts = data
        reset_records = [
            requisition for requisition in requisition_dicts
            if requisition['type'] == 'reset']

        for record in reset_records:
            data = record['data']

            tenants = await self._email_tenants(data['email'])
            user_anonymous = User (**AnonymousUser().__dict__)
            tenant_anonymous = Tenant(**AnonymousUser().__dict__)

            if not tenants:
                raise EmailExistsError(
                    f"The email not existing")

            multiple_links = []
            for tenant in tenants:
                tenant = Tenant(**tenant)
                token = self.verification_service.generate_token_tenant(
                    tenant, 'reset')
                config_url = self.config['url']
                url = (f'<a href=\"{config_url}'
                       f'/login/reset?verification_token='
                       f'{token.value}\">{tenant.name}</a><br>')
                multiple_links.append(url)

            await self.plan_supplier.notify(PasswordReset(**{
                'type': 'reset',
                'subject': 'Password Reset',
                'template': 'mail/auth/reset_pasword.html',
                'recipient': data['email'],
                'owner': data['email'].split('@')[0],
                'authorization': (
                    self.verification_service.generate_authorization(
                    tenant_anonymous, user_anonymous).value),
                'context':{
                    'user_name': data['email'].split('@')[0],
                    'unsubscribe_link': self.config['unsubscribe_link'],
                    'multiple_links': ''.join(multiple_links)
                }
            }))

        return {}

    async def verify(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        verification_dicts = data
        for record in verification_dicts:
            tenant = await self._session_tenant(record['tenant'])
            token_dict = await self.verification_service.verify(dict(record))
            [user] = await self.user_repository.search(
                [('email', '=', token_dict['temail'])])
            if token_dict['type'] == 'activation':
                user.active = True
                await self.user_repository.add(user)
            else:
                credential = Credential(value=record['data']['password'])
                await self.enrollment_service.set_credentials(
                    [user], [credential])
        return {}

    async def update(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        user_dicts = data
        credentials = [Credential(value=user_dict.pop('password', ''))
                       for user_dict in user_dicts]
        users = ([User(**user_dict) for user_dict in user_dicts])

        users = await self.user_repository.add(users)
        await self.enrollment_service.set_credentials(users, credentials)

        return {}

    async def deregister(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        user_ids = data
        users = await self.user_repository.search([('id', 'in', user_ids)])
        return {"data": await self.enrollment_service.deregister(users)}

    async def _session_tenant(self, tenant_name: str) -> Tenant:
        tenant_dict = self.tenant_supplier.resolve_tenant(tenant_name)
        tenant = Tenant(**tenant_dict)
        anonymouns_session = AnonymousUser(
            tid=tenant.id, tenant=tenant.slug,
            organization=tenant.name)
        self.auth_provider.setup(anonymouns_session)
        return tenant

    async def _email_tenants(self, email: str) -> list:
        tenants = self.tenant_supplier.search_tenants(
            [('email', '=', email)])
        anonymouns_session = User(**AnonymousUser().__dict__)
        self.auth_provider.setup(anonymouns_session)
        return tenants

    async def _ensure_dominion(self, dominion_name: str) -> Dominion:
        dominions = await self.dominion_repository.search(
            [('name', '=', dominion_name)])
        if not dominions:
            dominions = await self.dominion_repository.add(
               Dominion(name=dominion_name))
        [dominion] = dominions
        return dominion

    async def _generate_refresh_token(
        self, user_id: str, client: str) -> TokenString:
        refresh_payload = {'type': 'refresh_token',
                           'client': client,
                           'sub': user_id}
        refresh_token = self.refresh_token_service.generate_token(
            refresh_payload)

        # Remove previous refresh tokens as a user should have only one
        previous_tokens = await self.credential_repository.search([
            ('user_id', '=', user_id), ('type', '=', 'refresh_token'),
            ('client', '=', client)])
        for token in previous_tokens:
            await self.credential_repository.remove(token)

        credential = Credential(user_id=user_id,
                                value=refresh_token.value,
                                type='refresh_token', client=client)
        await self.credential_repository.add(credential)

        return refresh_token.value

    async def _find_user(self, username: str) -> User:
        domain: QueryDomain = [('username', '=', username)]
        if '@' in username:
            domain = [('email', '=', username)]

        users = await self.user_repository.search(domain)
        if not users:
            raise AuthError("Authentication Error: User not found.")
        return users[0]

    async def _password_authenticate(
            self, username: str, password: str,
        client: str, dominion_name: str, tenant_name: str) -> TokensDict:

        tenant = Tenant(
            **self.tenant_supplier.resolve_tenant(tenant_name))
        anonymouns_session = AnonymousUser(
            tid=tenant.id, tenant=tenant.slug,
            organization=tenant.name)
        self.auth_provider.setup(anonymouns_session)


        user = await self._find_user(username)
        credentials = await self.credential_repository.search([
            ('user_id', '=', user.id), ('type', '=', 'password')])

        if not credentials:
            raise AuthError("Authentication Error: No credentials found.")

        user_password = credentials[0].value
        if not self.hash_service.verify_password(password, user_password):
            raise AuthError("Authentication Error: Password mismatch.")

        dominion = await self._ensure_dominion(dominion_name)

        access_token = await self.access_service.generate_token(
            tenant, user, dominion)

        # Create new refresh token
        client = client or 'ALL'
        refresh_token_str = await self._generate_refresh_token(
            user.id, client)

        return {
            'refresh_token': refresh_token_str,
            'access_token': access_token.value
        }

    async def _provider_authenticate(
        self, username: str, password: str,
        client: str, dominion_name: str, tenant_name: str
    ) -> TokensDict:
        provider, code = username.replace(self.provider_pattern, ''), password

        tenant = Tenant(
            **self.tenant_supplier.resolve_tenant(tenant_name))
        anonymouns_session = AnonymousUser(
            tid=tenant.id, tenant=tenant.slug,
            organization=tenant.name)
        self.auth_provider.setup(anonymouns_session)

        user = await self.identity_service.identify(provider, code)

        [user] = await self.user_repository.search(
            [('email', '=', user.email)])

        dominion = await self._ensure_dominion(dominion_name)
        access_token = await self.access_service.generate_token(
            tenant, user, dominion)

        client = client or 'ALL'
        refresh_token_str = await self._generate_refresh_token(
            user.id, client)

        return {
            'refresh_token': refresh_token_str,
            'access_token': access_token.value
        }
