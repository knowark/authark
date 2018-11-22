from pytest import fixture, raises
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    CredentialRepository, MemoryCredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.reporters.authark_reporter import (
    AutharkReporter)


def test_authark_reporter_methods():
    methods = AutharkReporter.__abstractmethods__
    assert 'search_users' in methods
    assert 'search_credentials' in methods


def test_memory_authark_reporter_search_users_all(authark_reporter):
    domain = []
    users = authark_reporter.search_users(domain)

    assert len(users) == 3


def test_memory_authark_reporter_search_credentials_all(authark_reporter):
    domain = []
    credentials = authark_reporter.search_credentials(domain)

    assert len(credentials) == 3


def test_memory_authark_reporter_search_dominions_all(authark_reporter):
    domain = []
    dominions = authark_reporter.search_dominions(domain)

    assert len(dominions) == 1
