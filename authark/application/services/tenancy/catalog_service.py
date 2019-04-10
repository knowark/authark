from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .errors import AuthenticationError, AuthorizationError
from .token import Token
from .user import User


class CatalogService(ABC):
    """Authentication and authorization service."""
    class Roles:
        ADMIN = "ADMIN"
        MONITOR = "MONITOR"
        SUPERVISOR = "SUPERVISOR"
        GUARD = "GUARD"

    @abstractmethod
    def setup(self, auth_token: Token) -> None:
        """Setup the AuthService for the current user"""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if a user is authenticated"""

    @abstractmethod
    def validate_roles(self, required_roles: List[str]=None):
        """Check if a user is authenticated"""

    @abstractmethod
    def get_user(self) -> User:
        """Get the current request user"""


class MemoryAuthService(AuthService):

    def __init__(self) -> None:
        self.authenticated = False
        self.roles = []  # type: List[str]
        self.user = User(name="User")

    def setup(self, auth_token: Token) -> None:
        self.authenticated = bool(auth_token.value)

    def is_authenticated(self) -> bool:
        return self.authenticated

    def validate_roles(self, required_roles: List[str]=None) -> None:
        required_roles = required_roles or []
        required_roles.append(self.Roles.ADMIN)
        required_roles_set = set(required_roles)
        roles_set = set(self.roles)
        if not roles_set & required_roles_set:
            raise AuthorizationError("Unable to validate roles.")

    def get_user(self) -> User:
        return self.user

    def set_roles(self, roles: List[str]) -> None:
        self.roles = roles

    def get_roles(self) -> List[str]:
        if not self.is_authenticated():
            raise AuthenticationError("Authentication is required to "
                                      "get the user's roles.")
        return self.roles

    def load(self, token: str) -> None:
        self.token = token
