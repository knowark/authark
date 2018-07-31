from authark.application.repositories.user_repository import UserRepository
from authark.application.services.token_service import TokenService
from authark.application.services.hash_service import HashService
from authark.application.models.error import AuthError
from authark.application.models.token import Token
from authark.application.models.user import User


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 hash_service: HashService,
                 token_service: TokenService) -> None:
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.token_service = token_service

    def authenticate(self, username: str, password: str) -> Token:
        user = self.user_repository.get(username)

        if not (user and self.hash_service.verify_password(
                password, user.password)):
            raise AuthError("Authentication Error!")

        payload = {'user': user.username, 'email': user.email}

        token = self.token_service.generate_token(payload)

        return token

    def register(self, username: str, email: str, password: str) -> User:

        hashed_password = self.hash_service.generate_hash(password)

        user = User(username=username, email=email, password=hashed_password)
        self.user_repository.save(user)

        return user
