from ....application.repositories import UserRepository


class UserImporter():

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def import_(self, import_users):
        pass
