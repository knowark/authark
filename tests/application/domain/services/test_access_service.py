import json
from authark.application.domain.models import User, Tenant, Token, Dominion
from authark.application.domain.services import Tenant


async def test_access_service_generate_token(access_service) -> None:
    tenant = Tenant(id='T1', name='Default')
    user = User(id='U1', username='johndoe', email='johndoe')
    dominion = Dominion(id='D1', name='Data Server')

    token = await access_service.generate_token(tenant, user, dominion)

    assert isinstance(token, Token)


async def test_access_service_generate_token_payload(access_service) -> None:
    tenant = Tenant(id='T1', name='Default')
    user = User(id='U1', username='johndoe',
                name="John Doe",  email='johndoe')
    dominion = Dominion(id='D1', name='Data Server')

    token = await access_service.generate_token(tenant, user, dominion)

    assert token.value == json.dumps({
        "tid": "T1",
        "tenant": "default",
        "organization": "Default",
        "uid": "U1",
        "username": "johndoe",
        "name": "John Doe",
        "email": "johndoe",
        "attributes": {},
        "roles": []
    })


async def test_access_service_generate_token_roles(access_service) -> None:
    tenant = Tenant(id='1', name='Default')
    user = User(id='1', username='johndoe', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')

    user = User(id='1', username='johndoe', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')

    token = await access_service.generate_token(tenant, user, dominion)

    assert token.value == json.dumps({
        "tid": "1",
        "tenant": "default",
        "organization": "Default",
        "uid": "1",
        "username": "johndoe",
        "name": "",
        "email": "johndoe",
        "attributes": {},
        "roles": ['admin|1']
    })
