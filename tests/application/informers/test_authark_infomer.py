from authark.application.domain.common import QueryDomain
from authark.application.informers.authark_informer import AutharkInformer


def test_authark_informer_methods():
    methods = AutharkInformer.__abstractmethods__  # type: ignore
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


async def test_authark_informer_search_users_and_roles(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    items = await authark_informer.search(
        'user', domain, join='role', link='ranking')
    assert len(items) == 3
    assert items[0][0]['id'] == '1'
    assert items[0][1][0]['name'] == 'admin'
