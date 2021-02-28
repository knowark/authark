import json
from inspect import signature
from authark.application.domain.models.token import Token
from authark.application.domain.services import (
    TokenService, MemoryTokenService)


def test_token_service() -> None:
    methods = TokenService.__abstractmethods__  # type: ignore
    assert 'generate_token' in methods
    assert 'valid' in methods
    assert 'decode' in methods

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


def test_memory_token_service_valid() -> None:
    token_service = MemoryTokenService()
    token = Token('ACCESS')
    result = token_service.valid(token)

    assert result is True


def test_memory_token_service_decode() -> None:
    payload = {'user': "Pepe", 'email': "pepe@gmail.com"}

    token_service = MemoryTokenService()
    assert token_service.decode(Token(json.dumps(payload))) == payload
