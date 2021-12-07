from pytest import raises
from authark.application.domain.common import (
    UserCreationError, AuthError, RecordList)
from authark.application.domain.models import User, Credential


def test_auth_manager_creation(auth_manager):
    assert hasattr(auth_manager, 'authenticate')


async def test_auth_manager_authenticate(auth_manager):
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": "tebanep",
            "password": "PASS2",
            "client": "mobile"
        }
    }

    tokens = (await auth_manager.authenticate(request_dict))['data']

    assert isinstance(tokens, dict)
    assert 'refresh_token' in tokens.keys()
    assert 'access_token' in tokens.keys()


async def test_auth_manager_authenticate_new_dominion(auth_manager):
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "platformxyz",
            "tenant": "default",
            "username": "tebanep",
            "password": "PASS2",
            "client": "mobile"
        }
    }

    tokens = (await auth_manager.authenticate(request_dict))['data']
    dominions = await auth_manager.dominion_repository.search([])

    assert isinstance(tokens, dict)
    assert 'refresh_token' in tokens.keys()
    assert 'access_token' in tokens.keys()
    assert len(dominions) == 2
    assert 'default' in [dominion.name for dominion in dominions]
    assert 'platformxyz' in [dominion.name for dominion in dominions]


async def test_auth_manager_find_user_by_email(auth_manager):

    user = await auth_manager._find_user("tebanep@gmail.com")

    assert isinstance(user, User)
    assert user.id == '2'


async def test_auth_manager_find_user(auth_manager):

    user = await auth_manager._find_user("tebanep")

    assert isinstance(user, User)
    assert user.id == '2'


async def test_auth_manager_authenticate_no_credentials(auth_manager):
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default'] = {}
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": "tebanep",
            "password": "PASS2",
            "client": "mobile"
        }
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_refresh_authenticate_no_renewal(auth_manager):
    user_id = '1'
    refresh_token = "PREVIOUS_TOKEN"
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    tokens = (await auth_manager.authenticate({
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "refresh_token": refresh_token
        }
    }))['data']

    assert isinstance(tokens, dict)
    assert 'access_token' in tokens.keys()


async def test_auth_manager_refresh_authenticate_renewal(
        auth_manager, monkeypatch):
    user_id = '1'
    refresh_token = "PREVIOUS_TOKEN"
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    auth_manager.refresh_token_service.renew = (  # type: ignore
        lambda token: True)

    tokens = (await auth_manager.authenticate({
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "refresh_token": refresh_token
        }
    }))['data']

    assert isinstance(tokens, dict)
    assert 'access_token' in tokens.keys()
    assert 'refresh_token' in tokens.keys()


async def test_auth_manager_refresh_authenticate_refresh_token_not_found(
        auth_manager):
    user_id = '1'
    refresh_token = "GOOD_TOKEN"
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    with raises(AuthError):
        await auth_manager.authenticate({
            "meta": {},
            "data": {
                "dominion": "default",
                "tenant": "default",
                "refresh_token": "BAD_TOKEN"
            }
        })


async def test_generate_refresh_token(auth_manager):
    user_id = '1'
    client = 'mobile'
    refresh_token = await auth_manager._generate_refresh_token(
        user_id, client)
    credential_repository = auth_manager.credential_repository

    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 5


async def test_auth_manager_provider_authenticate(auth_manager):
    username = 'google@provider.oauth'
    password = 'AUTHORIZATION_CODE_1234'

    tokens = (await auth_manager.authenticate({
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": username,
            "password": password
        }
    }))['data']

    assert isinstance(tokens, dict)
    assert 'access_token' in tokens.keys()
    assert 'refresh_token' in tokens.keys()


async def test_generate_refresh_token_only_one(auth_manager):
    user_id = '1'
    client = 'mobile'
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value="PREVIOUS_TOKEN", type='refresh_token',
        client=client)

    assert len(credential_repository.data['default']) == 4
    refresh_token = await auth_manager._generate_refresh_token(
        user_id, client)
    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 4


async def test_auth_manager_fail_to_authenticate(auth_manager):
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": "tebanep",
            "password": "WRONG_PASSWORD",
            "client": "web"
        }
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_fail_to_authenticate_missing_user(auth_manager):
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": "MISSING_USER",
            "password": "WRONG_PASSWORD",
            "client": "web"
        }
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_fail_to_authenticate_missing_credentials(
        auth_manager):
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default'] = {}
    request_dict = {
        "meta": {},
        "data": {
            "dominion": "default",
            "tenant": "default",
            "username": "tebanep",
            "password": "NO_CREDENTIALS",
            "client": "terminal"
        }
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)
