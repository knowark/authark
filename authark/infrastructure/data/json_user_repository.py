from abc import ABC, abstractmethod
from json import load, dump
from typing import Dict, Optional
from authark.application.models.user import User
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
        data = {}
        with open(self.file_path, 'r') as f:
            data = load(f)
        data['users'].update({user.username: vars(user)})
        with open(self.file_path, 'w') as f:
            dump(data, f)
        return True
