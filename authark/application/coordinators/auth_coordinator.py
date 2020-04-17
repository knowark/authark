from ..models import Token, User, Credential, Dominion
from ..repositories import (
    UserRepository, CredentialRepository, DominionRepository)
from ..utilities import exceptions
from ..services import (
    TokenService, RefreshTokenService, HashService, AccessService)
from .types import TokenString, TokensDict, UserDict


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 hash_service: HashService,
                 access_service: AccessService,
                 refresh_token_service: RefreshTokenService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.hash_service = hash_service
        self.access_service = access_service
        self.refresh_token_service = refresh_token_service

    async def authenticate(self, username: str, password: str, client: str,
                           dominion_name: str = None) -> TokensDict:
        user = self._find_user(username)
        print("user en aut coor    ", user)
        credentials = await self.credential_repository.search([
            ('user_id', '=', user.id), ('type', '=', 'password')])

        if not credentials:
            raise AuthError("Authentication Error: No credentials found.")

        user_password = credentials[0].value
        if not await self.hash_service.verify_password(password, user_password):
            raise AuthError("Authentication Error: Password mismatch.")

        dominion_domain = [
            ('name', '=', dominion_name)] if dominion_name else []
        dominion: Dominion = next(
            iter(await self.dominion_repository.search(dominion_domain)))

        access_token = await self.access_service.generate_token(user, dominion)

        # Create new refresh token
        client = client or 'ALL'
        refresh_token_str = self._generate_refresh_token(user.id, client)

        return {
            'refresh_token': refresh_token_str,
            'access_token': access_token.value
        }

    async def refresh_authenticate(self, refresh_token: TokenString,
                                   dominion_name: str = None) -> TokensDict:
        credentials = await self.credential_repository.search([
            ('value', '=', refresh_token), ('type', '=', 'refresh_token')])
        if not credentials:
            raise AuthError("Authentication Error: Refresh token not found.")

        token = Token(refresh_token)
        await self.refresh_token_service.valid(token)

        tokens_dict = {}
        credential = credentials[0]

        if await self.refresh_token_service.renew(token):
            tokens_dict['refresh_token'] = self._generate_refresh_token(
                credential.user_id, credential.client)

        user = await self.user_repository.search(credential.user_id)

        dominion_domain = [
            ('name', '=', dominion_name)] if dominion_name else []
        dominion: Dominion = next(
            iter(await self.dominion_repository.search(dominion_domain)))

        tokens_dict['access_token'] = await self.access_service.generate_token(
            user, dominion).value

        return tokens_dict

    async def register(self, user_dict: UserDict) -> UserDict:
        user = User(**user_dict)

        self._validate_username(user.username)
        self._validate_duplicates(user)

        user = await self.user_repository.add(user).pop()
        self._make_password_credential(user.id, user_dict['password'])
        return vars(user)

    # async def update(self, user_dict: UserDict) -> bool:
    #     user = User(**user_dict)
    #     if 'password' in user_dict:
    #         self._make_password_credential(user.id, user_dict['password'])
    #     return await self.user_repository.update(user)

    async def deregister(self, user_id: str) -> bool:
        user = await self.user_repository.search(user_id)
        credentials = await self.credential_repository.search(
            [('user_id', '=', user.id)])
        for credential in credentials:
            await self.credential_repository.remove(credential)
        await self.user_repository.remove(user)

        return True

    async def _validate_username(self, username: str) -> None:
        if any((character in '@.+-_') for character in username):
            raise UserCreationError(
                f"The username '{username}' has forbidden characters")

    async def _validate_duplicates(self, user: User):
        users = await self.user_repository.search([
            '|', ('username', '=', user.username),
            ('email', '=', user.email)])

        for existing_user in users:
            message = f"A user with email '{user.email}' already exists."
            if user.username == existing_user.username:
                message = (
                    f"A user with username '{user.username}' already exists.")
            raise UserCreationError(message)

    async def _find_user(self, username: str):
        domain = [('username', '=', username)]
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
        refresh_token = await self.refresh_token_service.generate_token(
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

    async def _make_password_credential(self, user_id: str, password: str):
        credentials = await self.credential_repository.search([
            ('user_id', '=', user_id), ('type', '=', 'password')])
        for credential in credentials:
            await self.credential_repository.remove(credential)
        hashed_password = await self.hash_service.generate_hash(password)
        credential = Credential(user_id=user_id, value=hashed_password)
        await self.credential_repository.add(credential)
