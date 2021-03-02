from authark.application.domain.models import User, Token, Dominion
from authark.application.domain.services import Tenant


def test_verification_service_generate_token(
    verification_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')

    token = verification_service.generate_token(user)

    assert isinstance(token, Token)
    assert token.value == (
        '{"type": "activation", "tenant": "default", "uid": "1"}')


async def test_verification_service_verify(verification_service) -> None:
    verification_dict = {
        'tenant': 'default',
        'token': '{"type": "activation", "tenant": "default", "uid": "1"}'
    }

    await verification_service.verify(verification_dict)

    [user] = await verification_service.user_repository.search(
        [('id', '=', '1')])

    assert user.active is True
