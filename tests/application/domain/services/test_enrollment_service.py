from pytest import raises
from authark.application.domain.common import UserCreationError
from authark.application.domain.models import User, Credential, Token
from authark.application.domain.services import Tenant


async def test_enrollment_service_register(enrollment_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    credential = Credential(value='PLAIN_TEXT_PASSWORD')

    registration_tuples = [(user, credential)]

    [new_user] = await enrollment_service.register(registration_tuples)

    user_repository = enrollment_service.user_repository

    assert len(user_repository.data['default']) == 3
    assert user_repository.data['default'][new_user.id].username == 'johndoe'

    credential_repository = enrollment_service.credential_repository
    [new_credential] = await credential_repository.search(
        [('user_id', '=', '1')])
    assert new_credential.value == 'HASHED: PLAIN_TEXT_PASSWORD'


async def test_enrollment_service_set_credentials(enrollment_service) -> None:
    users = [User(id='1', username='johndoe', email='johndoe')]
    credentials = [Credential(value='PLAIN_TEXT_PASSWORD')]

    await enrollment_service.set_credentials(users, credentials)

    credential_repository = enrollment_service.credential_repository

    assert len(credential_repository.data['default']) == 4

    [new_credential] = await credential_repository.search(
        [('user_id', '=', '1')])

    assert len(new_credential.value)
    assert new_credential.value == 'HASHED: PLAIN_TEXT_PASSWORD'


async def test_enrollment_service_username_special_characters_error(
        enrollment_service):
    with raises(UserCreationError):
        user= User(**{
            "username": "mvp@gmail.com",
            "email": "mvp@gmail.com",
            "password": "PASS4"
        })
        enrollment_service._validate_usernames([user])


async def test_enrollment_servicer_register_duplicated_email_error(
        enrollment_service):
    user = User(**{
        "username": "mvp",
        "email": "mvp@gmail.com",
    })

    await enrollment_service.user_repository.add(user)

    new_user = User(**{
        "username": "mvp2",
        "email": "mvp@gmail.com",
    })

    with raises(UserCreationError):
        await enrollment_service._validate_duplicates([user])

async def test_enrollment_servicer_register_duplicated_username_error(
        enrollment_service):
    user = User(**{
        "username": "apv",
        "email": "apv@gmail.com",
    })

    await enrollment_service.user_repository.add(user)

    new_user = User(**{
        "username": "apv",
        "email": "other@gmail.com",
    })

    with raises(UserCreationError):
        await enrollment_service._validate_duplicates([user])


async def test_enrollment_service_deregister(enrollment_service):
    users = await enrollment_service.user_repository.search(
        [('id', '=', '2')])

    unregistered = await enrollment_service.deregister(users)

    credential_repository = enrollment_service.credential_repository
    user_repository = enrollment_service.user_repository

    assert unregistered is True
    assert len(user_repository.data['default']) == 2
    assert len(credential_repository.data['default']) == 3


async def test_enrollment_service_deregister_without_users(enrollment_service):
    unregistered = await enrollment_service.deregister([])
    credential_repository = enrollment_service.credential_repository
    user_repository = enrollment_service.user_repository

    assert unregistered is False
    assert len(user_repository.data['default']) == 3
    assert len(credential_repository.data['default']) == 4
