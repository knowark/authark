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

    def create_role(self, role_dict: RoleDict) -> None:
        role = Role(**role_dict)
        self.role_repository.add(role)
