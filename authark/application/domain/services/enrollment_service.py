from typing import Dict, List, Tuple, Any
from ..common import RecordList, UserCreationError
from ..models import User, Credential, Token, Dominion
from .repositories import UserRepository, CredentialRepository
from .hash_service import HashService


class EnrollmentService:
    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 hash_service: HashService) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.hash_service = hash_service

    async def register(
        self, registration_tuples: List[Tuple[User, Credential]]
    ) -> List[User]:

        users = [item[0] for item in registration_tuples]
        credentials = [item[1] for item in registration_tuples]

        self._validate_usernames(users)
        await self._validate_duplicates(users)

        users = await self.user_repository.add(users)

        await self.set_credentials(users, credentials)

        return users

    async def set_credentials(
            self, users: List[User], credentials: List[Credential]) -> None:
        new_credentials = []
        for user, credential in zip(users, credentials):
            hashed_password = self.hash_service.generate_hash(
                credential.value)
            credential = Credential(user_id=user.id, value=hashed_password)
            new_credentials.append(credential)

        old_credentials = await self.credential_repository.search([
            ('user_id', 'in', [user.id for user in users]),
            ('type', '=', 'password')])

        await self.credential_repository.remove(old_credentials)
        await self.credential_repository.add(new_credentials)

    async def deregister(self, users: List[User]) -> bool:
        if not users:
            return False

        credentials = await self.credential_repository.search(
            [('user_id', 'in', [user.id for user in users])])

        await self.credential_repository.remove(credentials)
        await self.user_repository.remove(users)

        return True

    def _validate_usernames(self, users: List[User]) -> None:
        for user in users:
            if any((character in '@.+-_') for character in user.username):
                raise UserCreationError(
                    f"The username '{user.name}' has forbidden characters")

    async def _validate_duplicates(self, users: List[User]):
        existing_users = await self.user_repository.search([
            '|', ('username', 'in', [user.username for user in users]),
            ('email', 'in',  [user.email for user in users])])

        for existing_user in existing_users:
            message = (
                f"A user with email '{existing_user.email}' or "
                f"username '{existing_user.name}' already exists.")
            raise UserCreationError(message)
