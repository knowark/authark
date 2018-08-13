import os
from abc import ABC, abstractmethod
from json import load, dump
from typing import Dict, List, Optional, Any
from authark.application.models.user import User
from authark.application.utilities.type_definitions import QueryDomain
from authark.application.repositories.user_repository import UserRepository


class JsonUserRepository(UserRepository):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get(self, username: str) -> Optional[User]:
        user = None
        with open(self.file_path) as f:
            data = load(f)
            users = data.get('users') or {}
            user = users.get(username)
            if user:
                user = User(**user)
        return user

    def save_(self, user: User) -> bool:
        data = {}  # type: Dict[str, Any]
        with open(self.file_path, 'r') as f:
            data = load(f)
        data['users'].update({user.username: vars(user)})
        with open(self.file_path, 'w') as f:
            dump(data, f)
        return True

    def search(self, domain: QueryDomain, limit=100, offset=0) -> List[User]:
        with open(self.file_path, 'r') as f:
            data = load(f)
            user_dict = data.get('users', {})

        users = [User(**user_dict) for user_dict in user_dict.values()]
        if limit:
            users = users[:limit]
        if offset:
            users = users[offset:]
        return users
