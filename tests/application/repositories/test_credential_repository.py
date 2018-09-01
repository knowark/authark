from typing import Dict
from pytest import fixture
from inspect import signature
from authark.application.models.credential import Credential
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.repositories.credential_repository import (
    MemoryCredentialRepository)


def test_credential_repository_methods() -> None:
    methods = CredentialRepository.__abstractmethods__
    assert 'get' in methods
    assert 'add' in methods
    assert 'search' in methods
    assert 'remove' in methods

    sig = signature(CredentialRepository.add)
    assert sig.parameters.get('credential')


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryCredentialRepository, CredentialRepository)


@fixture
def memory_credential_repository() -> MemoryCredentialRepository:
    credentials_dict = {
        "1": Credential(id='1', user_id='1', value="PASS1"),
        "2": Credential(id='2', user_id='2', value="PASS2"),
        "3": Credential(id='3', user_id='3', value="PASS3"),
    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(parser)
    credential_repository.load(credentials_dict)
    return credential_repository


def test_memory_credential_repository_get(
        memory_credential_repository) -> None:
    credential = memory_credential_repository.get("1")

    assert credential and credential.user_id == "1"
    assert credential and credential.value == "PASS1"


def test_memory_credential_repository_add() -> None:
    parser = ExpressionParser()
    memory_credential_repository = MemoryCredentialRepository(parser)

    credential = Credential(id='4', user_id='4', value="PASS4")

    is_saved = memory_credential_repository.add(credential)

    assert len(memory_credential_repository.credentials_dict) == 1
    assert is_saved
    assert "4" in memory_credential_repository.credentials_dict.keys()
    assert credential in memory_credential_repository.credentials_dict.values()


def test_memory_credential_repository_search(memory_credential_repository):
    domain = [('user_id', '=', "3")]

    credentials = memory_credential_repository.search(domain)

    assert len(credentials) == 1
    for credential in credentials:
        assert credential.id == '3'
        assert credential.user_id == "3"


def test_memory_credential_repository_search_all(memory_credential_repository):
    credentials = memory_credential_repository.search([])

    assert len(credentials) == 3


def test_memory_credential_repository_search_limit(
        memory_credential_repository):
    credentials = memory_credential_repository.search([], limit=2)

    assert len(credentials) == 2


def test_memory_user_repository_search_offset(memory_credential_repository):
    users = memory_credential_repository.search([], offset=2)

    assert len(users) == 1


def test_memory_credential_repository_delete_true(
        memory_credential_repository):
    credential = memory_credential_repository.credentials_dict["2"]
    deleted = memory_credential_repository.remove(credential)

    assert deleted is True
    assert len(memory_credential_repository.credentials_dict) == 2
    assert "2" not in memory_credential_repository.credentials_dict


def test_memory_credential_repository_delete_false(
        memory_credential_repository):
    credential = Credential(**{'id': '6', 'user_id': 'MISSING', 'value': ''})
    deleted = memory_credential_repository.remove(credential)

    assert deleted is False
    assert len(memory_credential_repository.credentials_dict) == 3
