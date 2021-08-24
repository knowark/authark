from abc import ABC, abstractmethod
from typing import List, Optional
from contextvars import ContextVar
from .exceptions import AuthenticationError, AuthorizationError


class User:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.name = attributes.get('name', '')
        self.email = attributes.get('email', '')
        self.tid = attributes.get('tid', '')
        self.tenant = attributes.get('tenant', '')
        self.organization = attributes.get('organization', '')
        self.zone = attributes.get('zone', '')
        self.roles = attributes.get('roles', [])
        self.attributes = attributes.get('attributes', {})
        self.token = attributes.get('token', '')


class AuthProvider(ABC):
    @abstractmethod
    def setup(self, user: User) -> None:
        """Setup the AuthProvider for the current user"""

    @property
    @abstractmethod
    def user(self) -> User:
        """Get the current request user"""

    @property
    def reference(self) -> str:
        return self.user.id

    @property
    def location(self) -> str:
        return self.user.tid

    @property
    def zone(self) -> str:
        return self.user.zone


user_var: ContextVar[Optional[User]] = ContextVar('user', default=None)


class StandardAuthProvider(AuthProvider):

    def setup(self, user: User) -> None:
        user_var.set(user)

    @property
    def user(self) -> User:
        user = user_var.get()
        if not user:
            raise AuthenticationError("Not authenticated.")
        return user
