from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Any, overload
from ...domain.services.repositories import (
    UserRepository, CredentialRepository,
    DominionRepository, RoleRepository,
    RestrictionRepository, PolicyRepository, RankingRepository)
from ...domain.common import QueryDomain, DataDict, RecordList


class StandardInformer():
    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 restriction_repository: RestrictionRepository,
                 policy_repository: PolicyRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.restriction_repository = restriction_repository
        self.policy_repository = policy_repository
        self.ranking_repository = ranking_repository


    async def search(self, entry: dict) -> dict:
        meta = entry['meta']
        model = meta['model']
        domain = meta['domain']
        repository = getattr(self, f'{model}_repository')
        result = await repository.search(domain=domain)
        return {'data': [vars(item) for item in result]}

    async def count(self, entry: dict) -> dict:
        meta = entry['meta']
        model = meta['model']

        repository = getattr(self, f'{model}_repository')
        result = await repository.count(meta['domain'])
        return {'data': result}

    async def join(self, model: str, domain: QueryDomain = None,
                   join: str = None, link: str = None,
                   source: str = None, target: str = None
                   ) -> List[Tuple[DataDict, RecordList]]:

        repository = getattr(self, f'{model}_repository')
        reference = getattr(self, f'{join}_repository', None)
        pivot = getattr(self, f'{link}_repository', None)

        items = await repository.join(
            domain or [], join=reference, link=pivot,
            source=source, target=target)

        return [(vars(item[0]), [vars(i) for i in item[1]])
                for item in items]
