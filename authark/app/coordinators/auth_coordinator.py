from authark.app.repositories.user_repository import UserRepository
from authark.app.services.token_service import TokenService
from authark.app.models.error import AuthError
from authark.app.models.token import Token
from authark.app.models.user import User


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository,
                 token_service: TokenService) -> None:
        self.user_repository = user_repository
        self.token_service = token_service

    def authenticate(self, username: str, password: str) -> Token:
        user = self.user_repository.get(username)

        if not (user and user.password == password):
            raise AuthError("Authentication Error!")

        payload = {'user': user.username, 'email': user.email}

        token = self.token_service.generate_token(payload)

        return token

    def register(self, username: str, email: str, password: str) -> User:

        user = User(username=username, email=email, password=password)
        self.user_repository.save(user)

        return user
