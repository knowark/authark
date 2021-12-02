from authark.application.domain.models import User, Tenant, Token, Dominion
from authark.application.domain.services import Tenant


def test_verification_service_generate_token(
    verification_service) -> None:
    tenant = Tenant(id='1', name='Default')
    user = User(id='1', username='johndoe', email='johndoe')

    token = verification_service.generate_token(tenant, user, 'activation')

    assert isinstance(token, Token)
    assert token.value == (
        '{"type": "activation", "tenant": "default", '
        '"tid": "1", "uid": "1"}')

def test_verification_service_generate_token_tenant(
    verification_service) -> None:
    tenant = Tenant(id='1', name='Default', email='default@example.com')

    token = verification_service.generate_token_tenant(tenant, 'reset')

    assert isinstance(token, Token)
    assert token.value == (
        '{"type": "reset", "tenant": "default", '
        '"tid": "1", "temail": "default@example.com"}')

async def test_verification_service_verify(verification_service) -> None:
    verification_dict = {
        'tenant': 'default',
        'token': ('{"type": "activation", "tenant": "default", '
                  '"tid": "1", "uid": "1"}')
    }

    token = await verification_service.verify(verification_dict)

    assert token == {
        "type": "activation", "tenant": "default", "tid": "1", "uid": "1"
    }
