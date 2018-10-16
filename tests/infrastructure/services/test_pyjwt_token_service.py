import jwt
from pytest import fixture
from authark.application.models.token import Token
from authark.application.services.token_service import TokenService
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService


def test_pyjwt_token_service_implementation() -> None:
    assert issubclass(PyJWTTokenService, TokenService)


def test_pyjwt_token_service_generate_token_with_payload() -> None:
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'user': "Pepe", 'email': "pepe@gmail.com"}
    lifetime = 3600

    pyjwt_service = PyJWTTokenService(secret=secret, algorithm=algorithm,
                                      lifetime=3600)
    token = pyjwt_service.generate_token(payload)
    value = token.value

    decoded_payload = jwt.decode(value, secret, algorithms=[algorithm])

    assert isinstance(token, Token)
    assert value
    assert payload == decoded_payload
