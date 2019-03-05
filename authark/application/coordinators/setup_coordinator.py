from ..services import ImportService
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository, RankingRepository)
from ..models import User, Credential, Role, Ranking


class SetupCoordinator:
    def __init__(self, import_service: ImportService,
                 user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository) -> None:
        self.import_service = import_service
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository

    def import_users(self, filepath: str, source: str,
                     password_field: str) -> None:
        users_list = self.import_service.import_users(
            filepath, source, password_field)
        for user, credential, roles in users_list:

            existing_user = self._search_user(user)
            if existing_user:
                user = existing_user
                self.user_repository.update(user)
            else:
                user = self.user_repository.add(user)
            if credential:
                credential.user_id = user.id
                self._update_credential(credential)
            if roles:
                self._generate_ranking_user(roles, user)

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

    def _generate_ranking_user(self, roles: Role, user: User) -> None:
        for role in roles:
            domain = [('name', '=', role.name)]
            existing_role = self.role_repository.search(domain)
            if existing_role:
                domain_ranking = [('user_id', '=', user.id),
                                  ('role_id', '=', existing_role[0].id)]
                existing_ranking = self.ranking_repository.search(
                    domain_ranking)
                if not existing_ranking:
                    ranking = Ranking(user_id=user.id,
                                      role_id=existing_role[0].id)
                    self.ranking_repository.add(ranking)
