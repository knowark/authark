from typing import List, Dict
from ...domain.common import (
    TokenString, TokensDict, AuthError, AnonymousUser,
    UserCreationError, AuthProvider, RecordList, QueryDomain)
from ...domain.models import Token, User, Tenant, Credential, Dominion
from ...domain.services.repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ...domain.services import (
    RefreshTokenService, HashService, AccessService,
    VerificationService, IdentityService)
from ...general.suppliers import TenantSupplier


class AuthManager:
    def __init__(
        self, auth_provider: AuthProvider,
        user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        hash_service: HashService,
        access_service: AccessService,
        refresh_token_service: RefreshTokenService,
        identity_service: IdentityService,
        tenant_supplier: TenantSupplier
    ) -> None:
        self.auth_provider = auth_provider
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.hash_service = hash_service
        self.access_service = access_service
        self.refresh_token_service = refresh_token_service
        self.identity_service = identity_service
        self.tenant_supplier = tenant_supplier
        self.provider_pattern = '@provider.oauth'

    async def authenticate(self, request_dict: Dict[str, str]) -> TokensDict:
        data = request_dict
        tenant = data.get('tenant', '')
        dominion = data.get('dominion', '')
        refresh_token = data.get('refresh_token', '')
        username = data.get('username', '')
        password = data.get('password', '')
        client = data.get('client', '')

        if refresh_token:
            return await self._refresh_authenticate(
                refresh_token, dominion, tenant)
        elif username.endswith(self.provider_pattern):
            return await self._provider_authenticate(
                username, password, client, dominion, tenant)
        return await self._password_authenticate(
                username, password, client, dominion, tenant)

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

    async def _refresh_authenticate(
        self, refresh_token: TokenString,
        dominion_name: str, tenant_name: str) -> TokensDict:

        tenant = Tenant(
            **self.tenant_supplier.resolve_tenant(tenant_name))
        anonymouns_session = AnonymousUser(
            tid=tenant.id, tenant=tenant.slug,
            organization=tenant.name)
        self.auth_provider.setup(anonymouns_session)

        credentials = await self.credential_repository.search([
            ('value', '=', refresh_token), ('type', '=', 'refresh_token')])
        if not credentials:
            raise AuthError("Authentication Error: Refresh token not found.")

        token = Token(refresh_token)
        self.refresh_token_service.valid(token)

        tokens_dict = {}
        credential = credentials[0]

        tokens_dict['refresh_token'] = await self._generate_refresh_token(
            credential.user_id, credential.client)

        user = await self.user_repository.search(
            [('id', '=', credential.user_id)])

        dominion = await self._ensure_dominion(dominion_name)

        access_token = await self.access_service.generate_token(
            tenant, user[0], dominion)
        tokens_dict['access_token'] = access_token.value

        return tokens_dict

    async def _ensure_dominion(self, dominion_name: str) -> Dominion:
        dominions = await self.dominion_repository.search(
            [('name', '=', dominion_name)])
        if not dominions:
            dominions = await self.dominion_repository.add(
               Dominion(name=dominion_name))
        [dominion] = dominions
        return dominion

    async def _find_user(self, username: str) -> User:
        domain: QueryDomain = [('username', '=', username)]
        if '@' in username:
            domain = [('email', '=', username)]

        users = await self.user_repository.search(domain)
        if not users:
            raise AuthError("Authentication Error: User not found.")
        return users[0]

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
