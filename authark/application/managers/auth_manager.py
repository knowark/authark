from typing import List, Dict
from ..domain.common import (
    TokenString, TokensDict, AuthError,
    UserCreationError, RecordList, QueryDomain)
from ..domain.models import Token, User, Credential, Dominion
from ..domain.repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ..domain.services import (
    RefreshTokenService, HashService, AccessService, NotificationService)


class AuthManager:

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 hash_service: HashService,
                 access_service: AccessService,
                 notification_service: NotificationService,
                 refresh_token_service: RefreshTokenService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.hash_service = hash_service
        self.access_service = access_service
        self.notification_service = notification_service
        self.refresh_token_service = refresh_token_service

    async def authenticate(self, request_dict: Dict[str, str]) -> TokensDict:
        dominion = request_dict['dominion']
        refresh_token = request_dict.get('refresh_token', '')
        username = request_dict.get('username', '')
        password = request_dict.get('password', '')
        client = request_dict.get('client', '')

        if refresh_token:
            result = await self._refresh_authenticate(
                refresh_token, dominion)
        else:
            result = await self._password_authenticate(
                username, password, client, dominion)

        return result

    async def register(self, user_dicts: RecordList) -> None:
        users = ([User(**user_dict) for user_dict in user_dicts])

        self._validate_usernames(users)
        await self._validate_duplicates(users)

        users = await self.user_repository.add([
            User(**user_dict) for user_dict in user_dicts])

        await self._make_password_credentials(users, user_dicts)

    async def _password_authenticate(
            self, username: str, password: str,
            client: str, dominion_name: str) -> TokensDict:
        user = await self._find_user(username)
        credentials = await self.credential_repository.search([
            ('user_id', '=', user.id), ('type', '=', 'password')])

        if not credentials:
            raise AuthError("Authentication Error: No credentials found.")

        user_password = credentials[0].value
        if not self.hash_service.verify_password(password, user_password):
            raise AuthError("Authentication Error: Password mismatch.")

        dominion = await self._ensure_dominion(dominion_name)

        access_token = await self.access_service.generate_token(user, dominion)

        # Create new refresh token
        client = client or 'ALL'
        refresh_token_str = await self._generate_refresh_token(user.id, client)

        return {
            'refresh_token': refresh_token_str,
            'access_token': access_token.value
        }

    async def _refresh_authenticate(self, refresh_token: TokenString,
                                    dominion_name: str) -> TokensDict:
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
            user[0], dominion)
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

    async def update(self, user_dicts: RecordList) -> None:
        users = ([User(**user_dict) for user_dict in user_dicts])

        users = await self.user_repository.add([
            User(**user_dict) for user_dict in user_dicts])

        await self._make_password_credentials(users, user_dicts)

    async def deregister(self, user_ids: List[str]) -> bool:
        users = await self.user_repository.search([('id', 'in', user_ids)])
        if not users:
            return False

        credentials = await self.credential_repository.search(
            [('user_id', 'in', [user.id for user in users])])

        await self.credential_repository.remove(credentials)
        await self.user_repository.remove(users)

        return True

    def _validate_usernames(self, users: List[User]) -> None:
        for user in users:
            if any((character in '@.+-_') for character in user.username):
                raise UserCreationError(
                    f"The username '{user.name}' has forbidden characters")

    async def _validate_duplicates(self, users: List[User]):
        existing_users = await self.user_repository.search([
            '|', ('username', 'in', [user.username for user in users]),
            ('email', 'in',  [user.email for user in users])])

        for existing_user in existing_users:
            message = (
                f"A user with email '{existing_user.email}' or "
                f"username '{existing_user.name}' already exists.")
            raise UserCreationError(message)

    async def _find_user(self, username: str):
        domain: QueryDomain = [('username', '=', username)]
        if '@' in username:
            domain = [('email', '=', username)]

        users = await self.user_repository.search(domain)
        if not users:
            raise AuthError("Authentication Error: User not found.")
        return users[0]

    async def _generate_refresh_token(self, user_id: str, client: str
                                      ) -> TokenString:
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

    async def _make_password_credentials(
            self, users: List[User], user_dicts: RecordList) -> None:
        updated_users = []
        new_credentials = []
        for user, user_dict in zip(users, user_dicts):
            if not user_dict.get('password'):
                continue
            hashed_password = self.hash_service.generate_hash(
                user_dict['password'])
            credential = Credential(user_id=user.id, value=hashed_password)
            updated_users.append(user)
            new_credentials.append(credential)

        old_credentials = await self.credential_repository.search([
            ('user_id', 'in', [user.id for user in updated_users]),
            ('type', '=', 'password')])

        await self.credential_repository.remove(old_credentials)

        await self.credential_repository.add(new_credentials)
