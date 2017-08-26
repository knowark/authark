from authark.app.repositories.user_repository import UserRepository


class AuthCoordinator:

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def authenticate(self, username: str, passwd: str) -> None:
        pass
