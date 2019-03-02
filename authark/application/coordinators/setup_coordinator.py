from ..services import ImportService
from ..repositories import UserRepository, CredentialRepository
from ..models import User, Credential


class SetupCoordinator:
    def __init__(self, import_service: ImportService,
                 user_repository: UserRepository,
                 credential_repository: CredentialRepository) -> None:
        self.import_service = import_service
        self.user_repository = user_repository
        self.credential_repository = credential_repository

    def import_users(self, filepath: str, source: str, password_field) -> None:
        users_list = self.import_service.import_users(
            filepath, source, password_field)
        for user, credential in users_list:

            existing_user = self._search_user(user)
            if existing_user:
                user = existing_user
                self.user_repository.update(user)
            else:
                user = self.user_repository.add(user)
            if credential:
                credential.user_id = user.id
                self._update_credential(credential)

    def _search_user(self, user: User) -> User:
        domain = [
            ('external_source', '=', user.external_source),
            ('external_id', '=', user.external_id)
        ]
        if user.id:
            domain = [('id', '=', user.id)]
        user_result = self.user_repository.search(domain)
        if user_result:
            return user_result[0]
        return False

    def _update_credential(self, credential: Credential):
        domain = [
            ('user_id', '=', credential.user_id),
            ('type', '=', 'password')]

        existing_credential = self.credential_repository.search(domain)
        if existing_credential:
            credential.id = existing_credential[0].id
            result = self.credential_repository.update(credential)
        else:
            self.credential_repository.add(credential)
