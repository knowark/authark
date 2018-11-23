from ..models import Dominion
from ..repositories import DominionRepository
from ..services import IdService


class ManagementCoordinator:

    def __init__(self, dominion_repository: DominionRepository,
                 id_service: IdService) -> None:
        self.dominion_repository = dominion_repository
        self.id_service = id_service

    def create_dominion(self, dominion_dict) -> None:
        if 'id' not in dominion_dict:
            dominion_dict['id'] = self.id_service.generate_id()
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)
