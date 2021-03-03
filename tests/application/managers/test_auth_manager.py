from pytest import raises
from authark.application.domain.common import (
    UserCreationError, AuthError, RecordList)
from authark.application.domain.models import User, Credential


def test_auth_manager_creation(auth_manager):
    assert hasattr(auth_manager, 'authenticate')


async def test_auth_manager_authenticate(auth_manager):
    request_dict = {
        'dominion': 'default',
        'username': 'tebanep',
        'password': 'PASS2',
        'client': 'mobile'
    }

    tokens = await auth_manager.authenticate(request_dict)

    assert isinstance(tokens, dict)
    assert 'refresh_token' in tokens.keys()
    assert 'access_token' in tokens.keys()


async def test_auth_manager_authenticate_new_dominion(auth_manager):
    request_dict = {
        'dominion': 'platformxyz',
        'username': 'tebanep',
        'password': 'PASS2',
        'client': 'mobile'
    }

    tokens = await auth_manager.authenticate(request_dict)
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
        'dominion': 'default',
        'username': 'tebanep',
        'password': 'PASS2',
        'client': 'mobile'
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_refresh_authenticate_no_renewal(auth_manager):
    user_id = '1'
    refresh_token = "PREVIOUS_TOKEN"
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    tokens = await auth_manager.authenticate({
        'dominion': 'default',
        'refresh_token': refresh_token})

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

    tokens = await auth_manager.authenticate({
        'dominion': 'default',
        'refresh_token': refresh_token})

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
            'dominion': 'default',
            'refresh_token': "BAD_TOKEN"})


async def test_generate_refresh_token(auth_manager):
    user_id = '1'
    client = 'mobile'
    refresh_token = await auth_manager._generate_refresh_token(
        user_id, client)
    credential_repository = auth_manager.credential_repository

    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 4


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
        'dominion': 'default',
        'username': 'tebanep',
        'password': 'WRONG_PASSWORD',
        'client': 'web'
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_fail_to_authenticate_missing_user(auth_manager):
    request_dict = {
        'dominion': 'default',
        'username': 'MISSING_USER',
        'password': 'WRONG_PASSWORD',
        'client': 'web'
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_fail_to_authenticate_missing_credentials(
        auth_manager):
    credential_repository = auth_manager.credential_repository
    credential_repository.data['default'] = {}
    request_dict = {
        'dominion': 'default',
        'username': 'tebanep',
        'password': 'NO_CREDENTIALS',
        'client': 'terminal'
    }
    with raises(AuthError):
        await auth_manager.authenticate(request_dict)


async def test_auth_manager_register(auth_manager):
    user_dicts: RecordList = [{
        "id": "007",
        "name": "Miguel Vivas",
        "username": "mvp",
        "email": "mvp@gmail.com",
        "password": "PASS4"
    }]
    await auth_manager.register(user_dicts)
    credential_repository = auth_manager.credential_repository
    user_repository = auth_manager.user_repository
    notification_service = auth_manager.notification_service

    assert len(user_repository.data['default']) == 4
    [new_user] = await user_repository.search([('id', '=', '007')])
    assert new_user.username == 'mvp'
    assert new_user.active is False

    assert len(credential_repository.data['default']) == 4
    assert notification_service.notification == {
        'type': 'activation',
        'subject': 'Account Activation',
        'recipient': 'mvp@gmail.com',
        'owner': 'Miguel Vivas',
        'token': (
            '{"type": "activation", "tenant": "default", "uid": "007"}')
    }


async def test_auth_manager_update(auth_manager):
    user_dicts: RecordList = [{
        "id": "1",
        "username": "valenep",
        "email": "valenep@gmail.com",
        "password": "NEW: PASS1"
    }]

    await auth_manager.update(user_dicts)
    credential_repository = auth_manager.credential_repository
    user_repository = auth_manager.user_repository

    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 3
    assert user_repository.data['default']['1'].username == "valenep"
    assert "HASHED: NEW: PASS1" in [
        credential.value for credential in
        credential_repository.data['default'].values()]


async def test_auth_manager_update_without_password(auth_manager):
    user_dicts: RecordList = [{
        "id": "1",
        "username": "valenep",
        "email": "valenep@outlook.com",
    }]

    await auth_manager.update(user_dicts)
    credential_repository = auth_manager.credential_repository
    user_repository = auth_manager.user_repository

    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 3
    assert user_repository.data['default']['1'].username == "valenep"
    assert user_repository.data['default']['1'].email == "valenep@outlook.com"


async def test_auth_manager_register_username_special_characters_error(
        auth_manager):
    with raises(UserCreationError):
        user_dicts: RecordList = [{
            "username": "mvp@gmail.com",
            "email": "mvp@gmail.com",
            "password": "PASS4"
        }]
        await auth_manager.register(user_dicts)


async def test_auth_manager_register_duplicated_email_error(
        auth_manager):
    user_dicts: RecordList = [{
        "username": "mvp",
        "email": "mvp@gmail.com",
        "password": "PASS4"
    }]
    await auth_manager.register(user_dicts)
    user_dicts[0]['username'] = "mvp2"
    user_dicts[0]['email'] = "mvp@gmail.com"
    with raises(UserCreationError):
        await auth_manager.register(user_dicts)


async def test_auth_manager_register_duplicated_username_error(
        auth_manager):

    with raises(UserCreationError):
        user_dicts: RecordList = [{
            "username": "mvp",
            "email": "mvp@gmail.com",
            "password": "PASS4"
        }]
        await auth_manager.register(user_dicts)
        user_dicts[0]['username'] = "mvp"
        user_dicts[0]['email'] = "mvp2@gmail.com"
        await auth_manager.register(user_dicts)


async def test_auth_manager_deregister(
        auth_manager, mock_user_repository):
    user_ids = [user.id for user in
                await mock_user_repository.search([('id', '=', '2')])]

    unregistered = await auth_manager.deregister(user_ids)

    credential_repository = auth_manager.credential_repository
    user_repository = auth_manager.user_repository

    assert unregistered is True
    assert len(user_repository.data['default']) == 2
    assert len(credential_repository.data['default']) == 2


async def test_auth_manager_deregister_without_ids(
        auth_manager, mock_user_repository):

    user_ids = []
    unregistered = await auth_manager.deregister(user_ids)
    credential_repository = auth_manager.credential_repository
    user_repository = auth_manager.user_repository

    assert unregistered is False
    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 3
