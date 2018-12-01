from inspect import signature
from authark.application.models import User, Token
from authark.application.services import AccessService, StandardAccessService


def test_access_service() -> None:
    methods = AccessService.__abstractmethods__  # type: ignore
    assert 'generate_token' in methods

    sig = signature(AccessService.generate_token)
    assert sig.parameters.get('user')


def test_standard_access_service_implementation() -> None:
    assert issubclass(StandardAccessService, AccessService)


def test_standard_access_service_generate_token(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    token = access_service.generate_token(user)

    assert isinstance(token, Token)


def test_standard_access_service_build_payload(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    payload = access_service._build_payload(user)

    assert isinstance(payload, dict)
    assert 'sub' in payload
    assert 'email' in payload
    assert 'attributes' in payload
    assert 'authorization' in payload


def test_standard_access_service_build_basic_info(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    info = access_service._build_basic_info(user)

    assert isinstance(info, dict)
    assert info['sub'] == user.id
    assert info['email'] == user.email
    assert info['attributes'] == user.attributes


def test_standard_access_service_build_authorization(access_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    authorization = access_service._build_authorization(user)

    assert isinstance(authorization, dict)
    assert 'Data Server' in authorization
    assert 'admin' in authorization['Data Server']['roles']
