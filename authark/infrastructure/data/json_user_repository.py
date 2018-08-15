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

    def get(self, id: str) -> Optional[User]:
        user = None
        with open(self.file_path) as f:
            data = load(f)
            users = data.get('users') or {}
            user = users.get(id)
            if user:
                user = User(**user)
        return user

    def save_(self, user: User) -> bool:
        data = {}  # type: Dict[str, Any]
        with open(self.file_path, 'r') as f:
            data = load(f)
        data['users'].update({user.id: vars(user)})
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

    def delete(self, user: User) -> bool:
        with open(self.file_path, 'r') as f:
            data = load(f)
            users_dict = data.get('users')

        print("DATA ====>>", data)
        if user.id not in users_dict:
            return False

        del users_dict[user.id]

        print("uSERS DICT", users_dict)
        print("NEW DATA DICT", data, len(data['users']))

        with open(self.file_path, 'w') as f:
            dump(data, f)
        return True
