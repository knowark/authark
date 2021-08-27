from typing import Dict, Any
from ..domain.common.auth import (
    AuthProvider, User, AnonymousUser, SystemUser)


class SessionManager:
    def __init__(self, auth_provider: AuthProvider) -> None:
        self.auth_provider = auth_provider

    def get_user(self) -> Dict[str, Any]:
        current = self.auth_provider.user
        return vars(current)

    def set_user(self, entry: Dict[str, Any]) -> None:
        user: User = SystemUser()
        if entry.get('data'):
            user = User(**entry['data'])
        elif entry.get('meta', {}).get('anonymous'):
            user = AnonymousUser(**entry.get('data', {}))

        self.auth_provider.setup(user)
