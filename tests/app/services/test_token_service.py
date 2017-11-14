from inspect import signature
from authark.app.models.token import Token
from authark.app.services.token_service import TokenService
from authark.app.services.token_service import MemoryTokenService


def test_token_service() -> None:
    methods = TokenService.__abstractmethods__
    assert 'generate_token' in methods

    sig = signature(TokenService.generate_token)
    assert sig.parameters.get('payload')


def test_memory_token_service_implementation() -> None:
    assert issubclass(MemoryTokenService, TokenService)


def test_memory_token_service_generate_token_with_payload() -> None:
    payload = {'user': "Pepe", 'email': "pepe@gmail.com"}

    token_service = MemoryTokenService()
    token = token_service.generate_token(payload)
    value = token.value

    assert isinstance(token, Token)
    assert isinstance(value, str)
    assert "Pepe" in value
    assert "email" in value
