from ..models import Dominion, Role
from ..repositories import DominionRepository, RoleRepository
from ..services import IdService
from.types import DominionDict, RoleDict


class ManagementCoordinator:

    def __init__(self, dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 id_service: IdService) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.id_service = id_service

    def create_dominion(self, dominion_dict: DominionDict) -> None:
        if 'id' not in dominion_dict:
            dominion_dict['id'] = self.id_service.generate_id()
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)

    def create_role(self, role_dict: RoleDict) -> None:
        if 'id' not in role_dict:
            role_dict['id'] = self.id_service.generate_id()
        role = Role(**role_dict)
        self.role_repository.add(role)
