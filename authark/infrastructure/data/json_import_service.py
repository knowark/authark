import json
from ...application.repositories import CredentialRepository
from ...application.services import ImportService, HashService
from ...application.models import User, Credential


class JsonImportService(ImportService):

    def __init__(self, credential_repository: CredentialRepository,
                 hash_service: HashService) -> None:
        self.credential_repository = credential_repository
        self.hash_service = hash_service

    def import_users(self, filepath: str, source: str,
                     password_field: str) -> []:
        users_list = []
        with open(filepath) as f:
            users_dict = json.load(f)
            for user_key, user_dict in users_dict.get('users').items():
                user_dict_data = {
                    'external_source': source,
                    'external_id': user_key,
                    'username': user_dict.pop('username'),
                    'email': user_dict.pop('email', ''),
                    'name': user_dict.pop('name', ''),
                    'gender': user_dict.pop('gender', ''),
                    'attributes': user_dict
                }
                credential = None
                if user_dict.get(password_field, False):
                    hashed_password = self.hash_service.generate_hash(
                        user_dict.pop(password_field))
                    credential = Credential(value=hashed_password)
                user = User(**user_dict_data)
                users_list.append([user, credential])
        f.close()
        return users_list
