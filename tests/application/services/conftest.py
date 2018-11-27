from pytest import fixture
from authark.application.models import Dominion, Role, Ranking
from authark.application.services import StandardAccessService
from authark.application.repositories import (
    ExpressionParser,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository)


@fixture
def dominion_repository() -> DominionRepository:
    dominions_dict = {
        "1": Dominion(id='1', name='Data Server',
                      url="https://dataserver.nubark.com")
    }
    parser = ExpressionParser()
    dominion_repository = MemoryDominionRepository(parser)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def role_repository() -> RoleRepository:
    roles_dict = {
        "1": Role(id='1', name='admin', dominion_id='1',
                  description="Service's Administrator")
    }
    parser = ExpressionParser()
    role_repository = MemoryRoleRepository(parser)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def ranking_repository() -> RankingRepository:
    rankings_dict = {
        "1": Ranking(id='1', user_id='1', role_id='1',
                     description="Service's Administrator")
    }
    parser = ExpressionParser()
    ranking_repository = MemoryRankingRepository(parser)
    ranking_repository.load(rankings_dict)
    return ranking_repository


@fixture
def access_service(ranking_repository, role_repository, dominion_repository):
    return StandardAccessService(
        ranking_repository, role_repository, dominion_repository)
