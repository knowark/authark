from ..models import Dominion
from ..repositories import DominionRepository


class ManagementCoordinator:

    def __init__(self, dominion_repository: DominionRepository) -> None:
        self.dominion_repository = dominion_repository

    def create_dominion(self, dominion_dict) -> None:
        dominion = Dominion(**dominion_dict)
        self.dominion_repository.add(dominion)
