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
    print('Cred val>>>>', new_credential.value)
    assert new_credential.value == 'HASHED: PLAIN_TEXT_PASSWORD'

async def test_enrollment_service_set_credentials(enrollment_service) -> None:
    users = [User(id='1', username='johndoe', email='johndoe')]
    credentials = [Credential(value='PLAIN_TEXT_PASSWORD')]

    await enrollment_service.set_credentials(users, credentials)

    credential_repository = enrollment_service.credential_repository

    assert len(credential_repository.data['default']) == 3

    [new_credential] = await credential_repository.search(
        [('user_id', '=', '1')])

    assert len(new_credential.value)
    assert new_credential.value == 'HASHED: PLAIN_TEXT_PASSWORD'

