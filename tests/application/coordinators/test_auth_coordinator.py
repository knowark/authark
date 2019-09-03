from typing import Dict, cast
from pytest import fixture, raises
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.utilities import ExpressionParser, UserCreationError
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    CredentialRepository, MemoryCredentialRepository)
from authark.application.services.token_service import (
    TokenService, MemoryTokenService)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)
from authark.application.models.error import AuthError
from authark.application.models import User, Credential, Token


########
# TESTS
########
def test_auth_coordinator_creation(
        auth_coordinator: AuthCoordinator) -> None:
    assert hasattr(auth_coordinator, 'authenticate')


def test_auth_coordinator_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    tokens = auth_coordinator.authenticate("tebanep", "PASS2", 'mobile')

    assert isinstance(tokens, dict)
    assert 'refresh_token' in tokens.keys()
    assert 'access_token' in tokens.keys()


def test_auth_coordinator_find_user_by_email(
        auth_coordinator: AuthCoordinator) -> None:

    user = auth_coordinator._find_user("tebanep@gmail.com")

    assert isinstance(user, User)
    assert user.id == '2'


def test_auth_coordinator_find_user(
        auth_coordinator: AuthCoordinator) -> None:

    user = auth_coordinator._find_user("tebanep")

    assert isinstance(user, User)
    assert user.id == '2'


def test_auth_coordinator_update(
        auth_coordinator: AuthCoordinator) -> None:

    user_dict = {'id': '2', 'username': 'tebanep',
                 'email': 'newmail@eep.com', 'password': 'PASS'}
    updated = auth_coordinator.update(user_dict)

    assert updated is True
    items = getattr(auth_coordinator.user_repository, 'data')['default']
    assert items['2'].email == 'newmail@eep.com'

    # Testing without password

    user_dict = {'id': '2', 'username': 'tebanep',
                 'email': 'newmail@eep.com'}
    updated = auth_coordinator.update(user_dict)

    assert updated is True
    items = getattr(auth_coordinator.user_repository, 'data')['default']
    assert items['2'].email == 'newmail@eep.com'


def test_auth_coordinator_update_with_password(
        auth_coordinator: AuthCoordinator) -> None:

    user_dict = {'id': '2', 'username': 'tebanep',
                 'email': 'newmail@eep.com', 'password': 'newpass123'}
    updated = auth_coordinator.update(user_dict)

    assert updated is True
    users = getattr(auth_coordinator.user_repository, 'data')['default']
    assert users['2'].email == 'newmail@eep.com'

    credentials = auth_coordinator.credential_repository.search([
        ('user_id', '=', users['2'].id), ('type', '=', 'password')])
    assert credentials[0].value == 'HASHED: newpass123'


def test_auth_coordinator_authenticate_no_credentials(
        auth_coordinator: AuthCoordinator) -> None:
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default'] = {}
    with raises(AuthError):
        tokens = auth_coordinator.authenticate("tebanep", "PASS2", 'mobile')


def test_auth_coordinator_refresh_authenticate_no_renewal(
        auth_coordinator: AuthCoordinator) -> None:
    user_id = '1'
    refresh_token = "PREVIOUS_TOKEN"
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    tokens = auth_coordinator.refresh_authenticate(refresh_token)

    assert isinstance(tokens, dict)
    assert 'access_token' in tokens.keys()
    assert 'refresh_token' not in tokens.keys()


def test_auth_coordinator_refresh_authenticate_renewal(
        auth_coordinator: AuthCoordinator, monkeypatch) -> None:

    user_id = '1'
    refresh_token = "PREVIOUS_TOKEN"
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    auth_coordinator.refresh_token_service.renew = (  # type: ignore
        lambda token: True)

    tokens = auth_coordinator.refresh_authenticate(refresh_token)

    assert isinstance(tokens, dict)
    assert 'access_token' in tokens.keys()
    assert 'refresh_token' in tokens.keys()


def test_auth_coordinator_refresh_authenticate_refresh_token_not_found(
        auth_coordinator: AuthCoordinator) -> None:
    user_id = '1'
    refresh_token = "GOOD_TOKEN"
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value=refresh_token, type='refresh_token')

    with raises(AuthError):
        tokens = auth_coordinator.refresh_authenticate("BAD_TOKEN")


def test_generate_refresh_token(auth_coordinator: AuthCoordinator) -> None:
    user_id = '1'
    client = 'mobile'
    refresh_token = auth_coordinator._generate_refresh_token(user_id, client)
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)

    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 4


def test_generate_refresh_token_only_one(
        auth_coordinator: AuthCoordinator) -> None:
    user_id = '1'
    client = 'mobile'
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default']['4'] = Credential(
        id='4', user_id=user_id, value="PREVIOUS_TOKEN", type='refresh_token',
        client=client)

    assert len(credential_repository.data['default']) == 4
    refresh_token = auth_coordinator._generate_refresh_token(user_id, client)
    assert isinstance(refresh_token, str)
    assert len(credential_repository.data['default']) == 4


def test_auth_coordinator_fail_to_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    with raises(AuthError):
        token = auth_coordinator.authenticate("tebanep", "WRONG_PASSWORD",
                                              'web')


def test_auth_coordinator_fail_to_authenticate_missing_user(
        auth_coordinator: AuthCoordinator) -> None:

    with raises(AuthError):
        token = auth_coordinator.authenticate("MISSING_USER", "WRONG_PASSWORD",
                                              "web")


def test_auth_coordinator_fail_to_authenticate_missing_credentials(
        auth_coordinator: AuthCoordinator) -> None:
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    credential_repository.data['default'] = {}

    with raises(AuthError):
        token = auth_coordinator.authenticate("tebanep", "NO_CREDENTIALS",
                                              'terminal')


def test_auth_coordinator_register(
        auth_coordinator: AuthCoordinator) -> None:

    user_dict = {"username": "mvp", "email": "mvp@gmail.com",
                 "password": "PASS4"}
    user_dict = auth_coordinator.register(user_dict)
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    user_repository = cast(MemoryUserRepository,
                           auth_coordinator.user_repository)

    assert user_dict
    assert isinstance(user_dict, dict)
    assert len(user_repository.data['default']) == 4
    assert len(credential_repository.data['default']) == 4


def test_auth_coordinator_register_username_special_characters_error(
        auth_coordinator: AuthCoordinator) -> None:
    with raises(UserCreationError):
        user_dict = {"username": "mvp@gmail.com", "email": "mvp@gmail.com",
                     "password": "PASS4"}
        auth_coordinator.register(user_dict)


def test_auth_coordinator_register_duplicated_username_error(
        auth_coordinator: AuthCoordinator) -> None:
    with raises(UserCreationError):
        user_dict = {"username": "mvp", "email": "mvp@gmail.com",
                     "password": "PASS4"}
        auth_coordinator.register(user_dict)
        # user_dict['username'] = "mvp"
        # user_dict['email'] = "mvp@gmail.com"
        # auth_coordinator.register(user_dict)
        user_dict['username'] = "mvp2"
        user_dict['email'] = "mvp@gmail.com"
        auth_coordinator.register(user_dict)


def test_auth_coordinator_deregister(
        auth_coordinator: AuthCoordinator, mock_user_repository) -> None:

    user = mock_user_repository.get('2')
    unregistered = auth_coordinator.deregister(user.id)
    credential_repository = cast(MemoryCredentialRepository,
                                 auth_coordinator.credential_repository)
    user_repository = cast(MemoryUserRepository,
                           auth_coordinator.user_repository)

    assert unregistered is True
    assert len(user_repository.data['default']) == 2
    assert len(credential_repository.data['default']) == 2
