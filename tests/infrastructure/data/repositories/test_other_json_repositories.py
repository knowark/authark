from pytest import fixture
from unittest.mock import Mock
from authark.infrastructure.data import (
    JsonCredentialRepository, JsonDominionRepository,
    JsonRankingRepository, JsonRoleRepository, JsonUserRepository)
from authark.application.utilities import (
    ExpressionParser, StandardTenantProvider)


@fixture
def expresion_parser():
    return ExpressionParser()


@fixture
def tenant_provider():
    return StandardTenantProvider()


def test_json_credential_repository_instantiation(
        expresion_parser, tenant_provider):
    json_credential_repository = JsonCredentialRepository(
        "", expresion_parser, tenant_provider)
    assert isinstance(json_credential_repository, JsonCredentialRepository)


def test_json_dominion_repository_instantiation(
        expresion_parser, tenant_provider):
    json_dominion_repository = JsonDominionRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_dominion_repository, JsonDominionRepository)


def test_json_ranking_repository_instantiation(
        expresion_parser, tenant_provider):
    json_ranking_repository = JsonRankingRepository(
        "", expresion_parser, tenant_provider)
    assert isinstance(json_ranking_repository, JsonRankingRepository)


def test_json_role_repository_instantiation(
        expresion_parser, tenant_provider):
    json_role_repository = JsonRoleRepository(
        "", expresion_parser, tenant_provider)
    assert isinstance(json_role_repository, JsonRoleRepository)


def test_json_user_repository_instantiation(
        expresion_parser, tenant_provider):
    json_user_repository = JsonUserRepository(
        "", expresion_parser, tenant_provider)
    assert isinstance(json_user_repository, JsonUserRepository)
