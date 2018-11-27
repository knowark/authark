import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..models import User
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository)


class AccessService(ABC):
    @abstractmethod
    def generate_payload(self, user: User) -> Dict[str, str]:
        "Generate payload method to be implemented."


class StandardAccessService(AccessService):

    def __init__(self, ranking_repository: RankingRepository,
                 role_repository: RoleRepository,
                 dominion_repository: DominionRepository) -> None:
        self.ranking_repository = ranking_repository
        self.role_repository = role_repository
        self.dominion_repository = dominion_repository

    def generate_payload(self, user: User) -> Dict[str, Any]:
        payload = self._build_basic_info(user)
        payload['authorization'] = self._build_authorization(user)
        return payload

    def _build_basic_info(self, user: User) -> Dict[str, Any]:
        return {
            'sub': user.id,
            'email': user.email,
            'name': user.name,
            'gender': user.gender
        }

    def _build_authorization(self, user: User) -> Dict[str, Any]:
        authorization = {}  # type: Dict[str, Any]
        rankings = self.ranking_repository.search([('user_id', '=', user.id)])
        roles = self.role_repository.search([('id', 'in', [
            ranking.role_id for ranking in rankings])])
        dominions = self.dominion_repository.search([('id', 'in', [
            role.dominion_id for role in roles])])

        for dominion in dominions:
            authorization[dominion.name] = {
                "roles":  [role.name for role in roles
                           if role.dominion_id == dominion.id]
            }

        return authorization
