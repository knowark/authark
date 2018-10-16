from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.application.services.token_service import TokenService
from authark.application.services.hash_service import HashService
from authark.application.services.id_service import IdService
from authark.application.models.error import AuthError
from authark.application.models.token import Token
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.utilities.type_definitions import (
    TokenString, TokensDict, UserDict)


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 hash_service: HashService,
                 access_token_service: TokenService,
                 refresh_token_service: TokenService,
                 id_service: IdService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.hash_service = hash_service
        self.access_token_service = access_token_service
        self.refresh_token_service = refresh_token_service
        self.id_service = id_service

    def authenticate(self, username: str, password: str) -> TokensDict:
        users = self.user_repository.search([('username', '=', username)])
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

        access_payload = {'user': user.username, 'email': user.email}
        access_token = self.access_token_service.generate_token(access_payload)

        # Create new refresh token
        refresh_token_str = self._generate_refresh_token(user.id)

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
        user = self.user_repository.get(credential.user_id)

        if self.refresh_token_service.renew(token):
            tokens_dict['refresh_token'] = self._generate_refresh_token(
                user.id)

        access_payload = {'user': user.username, 'email': user.email}
        tokens_dict['access_token'] = self.access_token_service.generate_token(
            access_payload).value

        return tokens_dict

    def register(self, username: str, email: str, password: str) -> UserDict:
        hashed_password = self.hash_service.generate_hash(password)
        user_id = self.id_service.generate_id()

        user = User(id=user_id, username=username,
                    email=email)

        credential_id = self.id_service.generate_id()
        credential = Credential(id=credential_id, user_id=user_id,
                                value=hashed_password)
        self.user_repository.add(user)
        self.credential_repository.add(credential)

        return vars(user)

    def deregister(self, user_id: str) -> bool:
        user = self.user_repository.get(user_id)
        if not user:
            return False
        self.user_repository.remove(user)

        credentials = self.credential_repository.search(
            [('user_id', '=', user.id)])
        for credential in credentials:
            self.credential_repository.remove(credential)

        return True

    def _generate_refresh_token(self, user_id: str) -> TokenString:
        credential_id = self.id_service.generate_id()
        refresh_payload = {'type': 'refresh_token'}
        refresh_token = self.refresh_token_service.generate_token(
            refresh_payload)

        # Remove previous refresh tokens as a user should have only one
        previous_tokens = self.credential_repository.search([
            ('user_id', '=', user_id), ('type', '=', 'refresh_token')])
        for token in previous_tokens:
            self.credential_repository.remove(token)

        credential = Credential(credential_id, user_id, refresh_token.value,
                                type='refresh_token')
        self.credential_repository.add(credential)

        return refresh_token.value
