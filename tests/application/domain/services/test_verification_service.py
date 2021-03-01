from authark.application.domain.models import User, Token, Dominion
from authark.application.domain.services import Tenant


def test_verification_service_generate_token(
    verification_service) -> None:
    user = User(id='1', username='johndoe', email='johndoe')
    dominion = Dominion(id='1', name='Data Server')

    token = verification_service.generate_token(user)

    assert isinstance(token, Token)
    assert token.value == (
        '{"type": "activation", "tenant": "default", "user_id": "1"}')
