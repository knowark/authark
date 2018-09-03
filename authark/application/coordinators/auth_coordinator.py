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
    TokenString, UserDict)


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 hash_service: HashService,
                 token_service: TokenService,
                 id_service: IdService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.hash_service = hash_service
        self.token_service = token_service
        self.id_service = id_service

    def authenticate(self, username: str, password: str) -> TokenString:
        users = self.user_repository.search([('username', '=', username)])
        if not users:
            raise AuthError("Authentication Error: User not found.")

        user = users[0]
        credentials = self.credential_repository.search([
            ('user_id', '=', user.id), ('type', '=', 'password')])

        user_password = credentials[0].value
        if not self.hash_service.verify_password(password, user_password):
            raise AuthError("Authentication Error: Password mismatch.")

        payload = {'user': user.username, 'email': user.email}

        token = self.token_service.generate_token(payload)

        return token.value

    def register(self, username: str, email: str, password: str) -> UserDict:
        hashed_password = self.hash_service.generate_hash(password)
        user_id = self.id_service.generate_id()

        user = User(id=user_id, username=username,
                    email=email, password=hashed_password)

        credential_id = self.id_service.generate_id()
        credential = Credential(id=credential_id, user_id=user_id,
                                value=hashed_password)
        self.user_repository.save(user)
        self.credential_repository.add(credential)

        return vars(user)

    def deregister(self, user_id: str) -> bool:
        user = self.user_repository.get(user_id)
        if not user:
            return False
        self.user_repository.delete(user)

        credentials = self.credential_repository.search(
            [('user_id', '=', user.id)])
        for credential in credentials:
            self.credential_repository.remove(credential)

        return True
