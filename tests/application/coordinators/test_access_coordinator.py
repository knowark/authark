from inspect import signature
from authark.application.models import User, Token
from authark.application.services import Tenant
from authark.application.coordinators import AccessCoordinator


def test_access_coordinator_generate_token(access_coordinator) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    token = access_coordinator.generate_token(user)

    assert isinstance(token, Token)


def test_access_coordinator_build_payload(access_coordinator) -> None:
    tenant = Tenant(name='Default')
    user = User(id='1', username='johndoe', email='johndoe')
    payload = access_coordinator._build_payload(tenant, user)

    assert isinstance(payload, dict)
    assert 'tid' in payload
    assert 'uid' in payload
    assert 'name' in payload
    assert 'email' in payload
    assert 'attributes' in payload
    assert 'authorization' in payload


def test_access_coordinator_build_basic_info(access_coordinator) -> None:
    tenant = Tenant(id='1', name='Default')
    user = User(id='1', username='johndoe', email='johndoe')
    info = access_coordinator._build_basic_info(tenant, user)

    assert isinstance(info, dict)
    assert info['tid'] == tenant.id
    assert info['uid'] == user.id
    assert info['name'] == user.name
    assert info['email'] == user.email
    assert info['attributes'] == user.attributes


def test_access_coordinator_build_authorization(access_coordinator) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    authorization = access_coordinator._build_authorization(user)

    assert isinstance(authorization, dict)
    assert 'Data Server' in authorization
    assert 'admin' in authorization['Data Server']['roles']


def test_access_coordinator_build_permissions(access_coordinator) -> None:
    dominion = access_coordinator.dominion_repository.get('1')
    roles = [access_coordinator.role_repository.get('1')]

    permissions_dict = access_coordinator._build_permissions(dominion, roles)

    assert isinstance(permissions_dict, dict)
    assert permissions_dict == {
        'employees': [
            {'type': 'role', 'name': 'First Role Only', 'value': '1'}
        ]
    }
