from unittest.mock import Mock
from authark.infrastructure.data import (
    JsonCredentialRepository, JsonDominionRepository, JsonGrantRepository,
    JsonPermissionRepository, JsonPolicyRepository, JsonRankingRepository,
    JsonResourceRepository, JsonRoleRepository, JsonUserRepository)

# TODO: replace mocks with real values.


def test_json_credential_repository_instantiation():
    json_credential_repository = JsonCredentialRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_credential_repository, JsonCredentialRepository)


def test_json_dominion_repository_instantiation():
    json_dominion_repository = JsonDominionRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_dominion_repository, JsonDominionRepository)


def test_json_grant_repository_instantiation():
    json_grant_repository = JsonGrantRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_grant_repository, JsonGrantRepository)


def test_json_permission_repository_instantiation():
    json_permission_repository = JsonPermissionRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_permission_repository, JsonPermissionRepository)


def test_json_policy_repository_instantiation():
    json_policy_repository = JsonPolicyRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_policy_repository, JsonPolicyRepository)


def test_json_ranking_repository_instantiation():
    json_ranking_repository = JsonRankingRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_ranking_repository, JsonRankingRepository)


def test_json_resource_repository_instantiation():
    json_resource_repository = JsonResourceRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_resource_repository, JsonResourceRepository)


def test_json_role_repository_instantiation():
    json_role_repository = JsonRoleRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_role_repository, JsonRoleRepository)


def test_json_user_repository_instantiation():
    json_user_repository = JsonUserRepository(
        Mock(), Mock(), Mock())
    assert isinstance(json_user_repository, JsonUserRepository)
