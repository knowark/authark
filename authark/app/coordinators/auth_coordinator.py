from authark.app.repositories.user_repository import UserRepository
from authark.app.models.user import User


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_repository.get(username)

        authenticated = False
        if user and user.password == password:
            authenticated = True

        return authenticated

    def register(self, username: str, email: str, password: str) -> User:

        user = User(username=username, email=email, password=password)
        self.user_repository.save(user)

        return user
