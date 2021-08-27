from abc import ABC, abstractmethod
from typing import List, Optional
from contextvars import ContextVar
from .exceptions import AuthenticationError, AuthorizationError


class User:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.username = attributes.get('username', '')
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
        return self.user.tenant

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


ZeroID = '00000000-0000-0000-0000-000000000000'


OneID = '11111111-1111-1111-1111-111111111111'


class AnonymousUser(User):
    def __init__(self, **attributes) -> None:
        self.id = ZeroID,
        self.name = 'anonymous',
        self.tid = ZeroID
        self.tenant = 'anonymous'
        super().__init__(**attributes)


class SystemUser(User):
    def __init__(self, **attributes) -> None:
        self.id = OneID,
        self.name = 'system',
        self.tid = OneID
        self.tenant = 'system'
        super().__init__(**attributes)
