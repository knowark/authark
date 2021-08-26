from authark.application.domain.models import User, Token, Dominion
from authark.application.domain.services import Tenant


async def test_access_service_generate_token(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')

    token = await access_service.generate_token(user, dominion)

    assert isinstance(token, Token)


async def test_access_service_build_payload(access_service) -> None:
    # tenant = Tenant(name='Default')
    user = User(id='1', username='johndoe', tid='T1', organization='Default',
                tenant='default', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')
    payload = await access_service._build_payload(user, dominion)

    assert isinstance(payload, dict)
    assert 'tid' in payload
    assert 'uid' in payload
    assert 'organization' in payload
    assert 'tenant' in payload
    assert 'username' in payload
    assert 'name' in payload
    assert 'email' in payload
    assert 'attributes' in payload
    assert 'roles' in payload


def test_access_service_build_basic_info(access_service) -> None:
    tenant = Tenant(id='1', name='Default')
    user = User(id='1', username='johndoe', email='johndoe')
    info = access_service._build_basic_info(tenant, user)

    assert isinstance(info, dict)
    assert info['tid'] == tenant.id
    assert info['uid'] == user.id
    assert info['organization'] == tenant.name
    assert info['tenant'] == tenant.slug
    assert info['username'] == user.username
    assert info['name'] == user.name
    assert info['email'] == user.email
    assert info['attributes'] == user.attributes


async def test_access_service_build_roles(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')

    roles = await access_service._build_roles(user, dominion)
    assert isinstance(roles, list)

    assert 'admin|1' in roles
