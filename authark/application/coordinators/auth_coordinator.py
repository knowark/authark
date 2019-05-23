
from ..models import AuthError, Token, User, Credential
from ..repositories import UserRepository, CredentialRepository
from ..utilities import UserCreationError
from ..services import (
    TokenService, RefreshTokenService, HashService, AccessService)
from .types import TokenString, TokensDict, UserDict


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 hash_service: HashService,
                 access_service: AccessService,
                 refresh_token_service: RefreshTokenService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.hash_service = hash_service
        self.access_service = access_service
        self.refresh_token_service = refresh_token_service

    def authenticate(self, username: str, password: str, client: str
                     ) -> TokensDict:
        domain = [('username', '=', username)]
        if '@' in username:
            domain = [('email', '=', username)]

        users = self.user_repository.search(domain)
        if not users:
            raise AuthError("Authentication Error: User not found.")

        user = users[0]
        credentials = self.credential_repository.search([
            ('user_id', '=', user.id), ('type', '=', 'password')])

        if not credentials:
            raise AuthError("Authentication Error: No credentials found.")

        user_password = credentials[0].value
        if not self.hash_service.verify_password(password, user_password):
            raise AuthError("Authentication Error: Password mismatch.")

        access_token = self.access_service.generate_token(user)

        # Create new refresh token
        client = client or 'ALL'
        refresh_token_str = self._generate_refresh_token(user.id, client)

        return {
            'refresh_token': refresh_token_str,
            'access_token': access_token.value
        }

    def refresh_authenticate(self, refresh_token: TokenString) -> TokensDict:
        credentials = self.credential_repository.search([
            ('value', '=', refresh_token), ('type', '=', 'refresh_token')])
        if not credentials:
            raise AuthError("Authentication Error: Refresh token not found.")

        token = Token(refresh_token)
        self.refresh_token_service.valid(token)

        tokens_dict = {}
        credential = credentials[0]

        if self.refresh_token_service.renew(token):
            tokens_dict['refresh_token'] = self._generate_refresh_token(
                credential.user_id, credential.client)

        user = self.user_repository.get(credential.user_id)

        tokens_dict['access_token'] = self.access_service.generate_token(
            user).value

        return tokens_dict

    def register(self, user_dict: UserDict) -> UserDict:
        user = User(**user_dict)

        if any((character in '@.+-_') for character in user.username):
            raise UserCreationError(
                f"The username '{user.username}' has forbidden characters")

        users = self.user_repository.search([
            '|', ('username', '=', user.username),
            ('email', '=', user.email)])

        for existing_user in users:
            message = f"A user with email '{user.email}' already exists."
            if user.username == existing_user.username:
                message = (
                    f"A user with username '{user.username}' already exists.")
            raise UserCreationError(message)

        user = self.user_repository.add(user)
        hashed_password = self.hash_service.generate_hash(
            user_dict['password'])
        credential = Credential(user_id=user.id, value=hashed_password)
        self.credential_repository.add(credential)
        return vars(user)

    def update(self, user_dict: UserDict) -> bool:
        user = User(**user_dict)
        return self.user_repository.update(user)

    def deregister(self, user_id: str) -> bool:
        user = self.user_repository.get(user_id)
        credentials = self.credential_repository.search(
            [('user_id', '=', user.id)])
        for credential in credentials:
            self.credential_repository.remove(credential)
        self.user_repository.remove(user)

        return True

    def _generate_refresh_token(self, user_id: str, client: str
                                ) -> TokenString:
        refresh_payload = {'type': 'refresh_token',
                           'client': client,
                           'sub': user_id}
        refresh_token = self.refresh_token_service.generate_token(
            refresh_payload)

        # Remove previous refresh tokens as a user should have only one
        previous_tokens = self.credential_repository.search([
            ('user_id', '=', user_id), ('type', '=', 'refresh_token'),
            ('client', '=', client)])
        for token in previous_tokens:
            self.credential_repository.remove(token)

        credential = Credential(user_id=user_id,
                                value=refresh_token.value,
                                type='refresh_token', client=client)
        self.credential_repository.add(credential)

        return refresh_token.value
