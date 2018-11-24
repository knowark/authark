from ..models import Dominion, Role
from ..repositories import DominionRepository, RoleRepository
from.types import DominionDict, RoleDict


class ManagementCoordinator:

    def __init__(self, dominion_repository: DominionRepository,
                 role_repository: RoleRepository) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository

    def create_dominion(self, dominion_dict: DominionDict) -> None:
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)

    def remove_dominion(self, dominion_id: str) -> bool:
        dominion = self.dominion_repository.get(dominion_id)
        if not dominion:
            return False
        self.dominion_repository.remove(dominion)
        return True

    def create_role(self, role_dict: RoleDict) -> None:
        role = Role(**role_dict)
        self.role_repository.add(role)

    def remove_role(self, role_id: str) -> bool:
        role = self.role_repository.get(role_id)
        if not role:
            return False
        self.role_repository.remove(role)
        return True
