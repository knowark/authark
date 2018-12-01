import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..models import User, Token
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository)
from ..services import AccessTokenService


class AccessService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> Token:
        "Generate payload method to be implemented."


class StandardAccessService(AccessService):

    def __init__(self, ranking_repository: RankingRepository,
                 role_repository: RoleRepository,
                 dominion_repository: DominionRepository,
                 token_service: AccessTokenService) -> None:
        self.ranking_repository = ranking_repository
        self.role_repository = role_repository
        self.dominion_repository = dominion_repository
        self.token_service = token_service

    def generate_token(self, user: User) -> Token:
        access_payload = self._build_payload(user)
        access_token = self.token_service.generate_token(access_payload)

        return access_token

    def _build_payload(self, user: User) -> Dict[str, Any]:
        payload = self._build_basic_info(user)
        payload['authorization'] = self._build_authorization(user)
        return payload

    def _build_basic_info(self, user: User) -> Dict[str, Any]:
        return {
            'sub': user.id,
            'email': user.email,
            'name': user.name,
            'gender': user.gender,
            'attributes': user.attributes
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
