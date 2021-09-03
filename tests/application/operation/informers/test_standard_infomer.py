from authark.application.domain.common import QueryDomain
from authark.application.operation.informers.standard_informer import (
    StandardInformer)

async def test_standard_informer_search_users(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    users = await standard_informer.search(
    {'meta': dict(model='user', domain=domain)})
    assert len(users['data']) == 3


async def test_standard_informer_search_credentials(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    credentials = await standard_informer.search(
    {'meta': dict(model='credential', domain=domain)})
    assert len(credentials['data']) == 3


async def test_standard_informer_search_dominions(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    dominions = await standard_informer.search(
    {'meta': dict(model='dominion', domain=domain)})
    assert len(dominions) == 1


async def test_standard_informer_search_roles(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    roles = await standard_informer.search(
    {'meta': dict(model='role', domain=domain)})
    assert len(roles) == 1


async def test_standard_informer_count_users(
        standard_informer: StandardInformer) -> None:
    users_count = await standard_informer.count(
    {'meta': dict(model='user', domain=[])})
    assert users_count['data'] == 3


async def test_standard_informer_join_users_and_roles(
        standard_informer: StandardInformer) -> None:
    domain: QueryDomain = []
    items = await standard_informer.join({
        "meta":{
            "model": "user",
            "domain": domain,
            "join": "role",
            "link": "ranking"
        }
        })
    assert len(items['data']) == 3
    assert items['data'][0][0]['id'] == '1'
    assert items['data'][0][1][0]['name'] == 'admin'
