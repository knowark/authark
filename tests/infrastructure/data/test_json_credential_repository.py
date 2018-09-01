from json import dumps, loads
from pytest import fixture
from authark.application.models.credential import Credential
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.infrastructure.data.json_credential_repository import (
    JsonCredentialRepository)


@fixture
def credential_repository(tmpdir) -> JsonCredentialRepository:
    credentials_dict = {
        "1": vars(Credential(id='1', user_id='1', value="PASS1")),
        "2": vars(Credential(id='2', user_id='2', value="PASS2")),
        "3": vars(Credential(id='3', user_id='3', value="PASS3")),
    }

    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))
    with open(file_path, 'w') as f:
        data = dumps({'credentials': credentials_dict})
        f.write(data)

    parser = ExpressionParser()
    credential_repository = JsonCredentialRepository(file_path=file_path,
                                                     parser=parser)

    return credential_repository


def test_json_credential_repository_implementation() -> None:
    assert issubclass(JsonCredentialRepository, CredentialRepository)


def test_json_credential_repository_get(
        credential_repository: JsonCredentialRepository) -> None:

    credential = credential_repository.get("1")

    assert credential and credential.user_id == "1"
    assert credential and credential.value == "PASS1"


def test_json_credential_repository_add(
        credential_repository: JsonCredentialRepository) -> None:

    credential = Credential('4', '4', "PASS4")
    credential_repository.add(credential)

    file_path = credential_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        credentials_dict = data.get("credentials")

        credentials_dict = credentials_dict.get('4')

        assert credentials_dict.get('id') == credential.id
        assert credentials_dict.get('user_id') == credential.user_id
        assert credentials_dict.get('value') == credential.value


def test_json_credential_repository_search(credential_repository):
    domain = [('user_id', '=', "3")]

    credentials = credential_repository.search(domain)

    assert len(credentials) == 1
    for credential in credentials:
        assert credential.id == '3'
        assert credential.user_id == "3"


def test_json_credential_repository_search_all(credential_repository):
    credentials = credential_repository.search([])

    assert len(credentials) == 3


def test_json_credential_repository_search_limit(credential_repository):
    credentials = credential_repository.search([], limit=2)

    assert len(credentials) == 2


def test_json_credential_repository_search_offset(credential_repository):
    credentials = credential_repository.search([], offset=2)

    assert len(credentials) == 1


def test_json_credential_repository_delete_true(credential_repository):
    file_path = credential_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        credentials_dict = data.get("credentials")
        credentials_dict = credentials_dict.get('2')

    credential = Credential(**credentials_dict)
    deleted = credential_repository.remove(credential)

    with open(file_path) as f:
        data = loads(f.read())
        credentials_dict = data.get("credentials")

    assert deleted is True
    assert len(credentials_dict) == 2
    assert "2" not in credentials_dict.keys()


def test_json_credential_repository_delete_false(credential_repository):
    file_path = credential_repository.file_path
    credential = Credential(**{'id': '5', 'user_id': 'MISSING', 'value': ''})
    deleted = credential_repository.remove(credential)

    with open(file_path) as f:
        data = loads(f.read())
        credentials_dict = data.get("credentials")

    assert deleted is False
    assert len(credentials_dict) == 3
