from typing import Dict, Any, List
from ..models import User, Token, Dominion
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository)
from ..common import TenantProvider, Tenant
from .token_service import AccessTokenService


class AccessService:

    def __init__(self, ranking_repository: RankingRepository,
                 role_repository: RoleRepository,
                 dominion_repository: DominionRepository,
                 token_service: AccessTokenService,
                 tenant_provider: TenantProvider) -> None:
        self.ranking_repository = ranking_repository
        self.role_repository = role_repository
        self.dominion_repository = dominion_repository
        self.token_service = token_service
        self.tenant_provider = tenant_provider

    async def generate_token(self, user: User, dominion: Dominion) -> Token:
        tenant = self.tenant_provider.tenant
        access_payload = await self._build_payload(tenant, user, dominion)
        access_token = self.token_service.generate_token(access_payload)

        return access_token

    async def _build_payload(self, tenant: Tenant, user: User,
                             dominion: Dominion) -> Dict[str, Any]:
        payload = self._build_basic_info(tenant, user)
        if dominion:
            payload['roles'] = await self._build_roles(user, dominion)
        return payload

    def _build_basic_info(self, tenant: Tenant, user: User) -> Dict[str, Any]:
        return {
            'tid': tenant.id,
            'uid': user.id,
            'tenant': tenant.name,
            'name': user.name,
            'email': user.email,
            'attributes': user.attributes,
            'roles': []
        }

    async def _build_roles(self, user: User, dominion: Dominion) -> List[str]:
        dominion_roles = await self.role_repository.search(
            [('dominion_id', '=', dominion.id)])
        ranking_role_ids = [
            ranking.role_id for ranking in await self.ranking_repository.search(
                [('user_id', '=', user.id)])]
        roles = [role.name for role in dominion_roles
                 if role.id in ranking_role_ids]
        return roles
