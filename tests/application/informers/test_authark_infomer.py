from pytest import fixture, raises
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.repositories.memory_model_repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository)
from authark.application.utilities import QueryParser, QueryDomain
from authark.application.informers.authark_informer import (
    AutharkInformer)


def test_authark_informer_methods():
    methods = AutharkInformer.__abstractmethods__
    assert 'search' in methods
    assert 'count' in methods


async def test_authark_informer_search_users(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    users = await authark_informer.search('user', domain)
    assert len(users) == 3


async def test_authark_informer_search_credentials(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    credentials = await authark_informer.search('credential', domain)
    assert len(credentials) == 3


async def test_authark_informer_search_dominions(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    dominions = await authark_informer.search('dominion', domain)
    assert len(dominions) == 1


async def test_authark_informer_search_roles(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    roles = await authark_informer.search('role', domain)
    assert len(roles) == 1


async def test_authark_informer_count_users(
        authark_informer: AutharkInformer) -> None:
    users_count = await authark_informer.count('user')
    assert users_count == 3
