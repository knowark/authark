from authark.application.repositories.user_repository import UserRepository
from authark.application.services.token_service import TokenService
from authark.application.services.hash_service import HashService
from authark.application.services.id_service import IdService
from authark.application.models.error import AuthError
from authark.application.models.token import Token
from authark.application.models.user import User
from authark.application.utilities.type_definitions import (
    TokenString, UserDict)


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 hash_service: HashService,
                 token_service: TokenService,
                 id_service: IdService) -> None:
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.token_service = token_service
        self.id_service = id_service

    def authenticate(self, username: str, password: str) -> TokenString:
        user = self.user_repository.search([('username', '=', username)])[0]

        if not (user and self.hash_service.verify_password(
                password, user.password)):
            raise AuthError("Authentication Error!")

        payload = {'user': user.username, 'email': user.email}

        token = self.token_service.generate_token(payload)

        return token.value

    def register(self, username: str, email: str, password: str) -> UserDict:
        hashed_password = self.hash_service.generate_hash(password)
        id_ = self.id_service.generate_id()

        user = User(id=id_, username=username,
                    email=email, password=hashed_password)
        self.user_repository.save(user)

        return vars(user)

    def deregister(self, user_id: str) -> bool:
        user = self.user_repository.get(user_id)
        if not user:
            return False
        self.user_repository.delete(user)
        return True
