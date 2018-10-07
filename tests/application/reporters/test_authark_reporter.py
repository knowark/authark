from pytest import fixture, raises
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    CredentialRepository, MemoryCredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.reporters.authark_reporter import (
    AutharkReporter, MemoryAutharkReporter)


def test_authark_reporter_methods():
    methods = AutharkReporter.__abstractmethods__
    assert 'search_users' in methods
    assert 'search_credentials' in methods


@fixture
def user_repository() -> UserRepository:
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser)
    user_repository.load({
        "valenep": User('1', 'valenep', 'valenep@gmail.com'),
        "tebanep": User('2', 'tebanep', 'tebanep@gmail.com'),
        "gabeche": User('3', 'gabeche', 'gabeche@gmail.com')
    })
    return user_repository


@fixture
def credential_repository() -> CredentialRepository:
    credentials_dict = {
        "1": Credential(id='1', user_id='1', value="PASS1"),
        "2": Credential(id='2', user_id='2', value="PASS2"),
        "3": Credential(id='3', user_id='3', value="PASS3"),
    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(parser)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def authark_reporter(
        user_repository, credential_repository) -> AutharkReporter:
    return MemoryAutharkReporter(user_repository, credential_repository)


def test_memory_authark_reporter_search_users_all(authark_reporter):
    domain = []
    users = authark_reporter.search_users(domain)

    assert len(users) == 3


def test_memory_authark_reporter_search_credentials_all(authark_reporter):
    domain = []
    credentials = authark_reporter.search_credentials(domain)

    assert len(credentials) == 3
