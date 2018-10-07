from json import dumps, loads
from pytest import fixture
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.repositories.repository import Repository
from authark.application.reporters.authark_reporter import AutharkReporter
from authark.application.repositories.expression_parser import ExpressionParser
from authark.infrastructure.data.json_authark_reporter import (
    JsonAutharkReporter)
from authark.infrastructure.data.json_user_repository import (
    JsonUserRepository)
from authark.infrastructure.data.json_credential_repository import (
    JsonCredentialRepository)
from authark.infrastructure.data.init_json_database import init_json_database


@fixture(scope='session')
def authark_reporter(tmpdir_factory):
    file_path = str(
        tmpdir_factory.mktemp("authark", False).join('authark_data.json'))
    init_json_database(file_path)
    parser = ExpressionParser()
    user_repository = JsonUserRepository(file_path, parser)
    user_repository.add(User(**{
        'id': '1', 'username': 'mike', 'email': 'abc'}))
    credential_repository = JsonCredentialRepository(file_path, parser)
    credential_repository.add(Credential(**{
        'id': '1', 'user_id': '1', 'value': '123'}))
    return JsonAutharkReporter(user_repository, credential_repository)


def test_json_authark_reporter_implementation():
    assert issubclass(JsonAutharkReporter, AutharkReporter)


def test_json_authark_reporter_search_users(authark_reporter):
    domain = []
    result = authark_reporter.search_users(domain)
    assert len(result) == 1


def test_json_authark_reporter_search_credentials(authark_reporter):
    domain = []
    result = authark_reporter.search_credentials(domain)
    assert len(result) == 1
