import json
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from ..models import User, Token, Role, Dominion
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository,
    ResourceRepository, GrantRepository, PermissionRepository,
    PolicyRepository)
from ..services import AccessTokenService, TenantService, Tenant


class AccessCoordinator:

    def __init__(self, ranking_repository: RankingRepository,
                 role_repository: RoleRepository,
                 dominion_repository: DominionRepository,
                 resource_repository: ResourceRepository,
                 grant_repository: GrantRepository,
                 permission_repository: PermissionRepository,
                 policy_repository: PolicyRepository,
                 token_service: AccessTokenService,
                 tenant_service: TenantService) -> None:
        self.ranking_repository = ranking_repository
        self.role_repository = role_repository
        self.dominion_repository = dominion_repository
        self.resource_repository = resource_repository
        self.grant_repository = grant_repository
        self.permission_repository = permission_repository
        self.policy_repository = policy_repository
        self.token_service = token_service
        self.tenant_service = tenant_service

    def generate_token(self, user: User) -> Token:
        tenant = self.tenant_service.tenant
        access_payload = self._build_payload(tenant, user)
        access_token = self.token_service.generate_token(access_payload)

        return access_token

    def _build_payload(self, tenant: Tenant, user: User) -> Dict[str, Any]:
        payload = self._build_basic_info(tenant, user)
        payload['authorization'] = self._build_authorization(user)
        return payload

    def _build_basic_info(self, tenant: Tenant, user: User) -> Dict[str, Any]:
        return {
            'tid': tenant.id,
            'uid': user.id,
            'name': user.name,
            'email': user.email,
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
            role_names = [role.name for role in roles
                          if role.dominion_id == dominion.id]
            permissions_dict = self._build_permissions(dominion, roles)
            authorization[dominion.name] = {
                "roles":  role_names,
                "permissions": permissions_dict
            }

        return authorization

    def _build_permissions(self, dominion: Dominion,
                           roles: List[Role]) -> Dict[str, Any]:
        permissions = []
        for role in roles:
            permission_ids = [
                grant.permission_id for grant in self.grant_repository.search(
                    [('role_id', '=', role.id)])]
            permissions.extend(self.permission_repository.search(
                [('id', 'in', permission_ids)]))

        resources_dict = {
            resource.id: resource.name
            for resource in self.resource_repository.search(
                [('dominion_id', '=', dominion.id)])}

        permissions_dict: Dict[str, Any] = {}
        for permission in permissions:
            resource_name = resources_dict[permission.resource_id]
            policy_dict = vars(self.policy_repository.search(
                [('id', '=', permission.policy_id)])[0])
            del policy_dict['id']

            permissions_dict[resource_name] = (
                permissions_dict.get(resource_name, []))
            permissions_dict[resource_name].append(policy_dict)

        return permissions_dict
