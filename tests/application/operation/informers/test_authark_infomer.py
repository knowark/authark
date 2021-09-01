from authark.application.domain.common import QueryDomain
from authark.application.operation.informers.authark_informer import (
    AutharkInformer)


def test_authark_informer_methods():
    methods = AutharkInformer.__abstractmethods__  # type: ignore
    assert 'search' in methods
    assert 'count' in methods


async def test_authark_informer_search_users(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    users = await authark_informer.search(
    {'meta': dict(model='user', domain=domain)})
    assert len(users['data']) == 3


async def test_authark_informer_search_credentials(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    credentials = await authark_informer.search(
    {'meta': dict(model='credential', domain=domain)})
    assert len(credentials['data']) == 3


async def test_authark_informer_search_dominions(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    dominions = await authark_informer.search(
    {'meta': dict(model='dominion', domain=domain)})
    assert len(dominions) == 1


async def test_authark_informer_search_roles(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    roles = await authark_informer.search(
    {'meta': dict(model='role', domain=domain)})
    assert len(roles) == 1


async def test_authark_informer_count_users(
        authark_informer: AutharkInformer) -> None:
    users_count = await authark_informer.count(
    {'meta': dict(model='user', domain=[])})
    assert users_count['data'] == 3


async def test_authark_informer_join_users_and_roles(
        authark_informer: AutharkInformer) -> None:
    domain: QueryDomain = []
    items = await authark_informer.join(
        'user', domain, join='role', link='ranking')
    assert len(items) == 3
    assert items[0][0]['id'] == '1'
    assert items[0][1][0]['name'] == 'admin'
