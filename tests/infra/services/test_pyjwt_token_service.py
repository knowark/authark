import jwt
from pytest import fixture
from authark.app.models.token import Token
from authark.app.services.token_service import TokenService
from authark.infra.crypto.pyjwt_token_service import PyJWTTokenService


def test_pyjwt_token_service_implementation() -> None:
    assert issubclass(PyJWTTokenService, TokenService)


def test_pyjwt_token_service_generate_token_with_payload() -> None:
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'user': "Pepe", 'email': "pepe@gmail.com"}

    pyjwt_service = PyJWTTokenService(secret=secret, algorithm=algorithm)
    token = pyjwt_service.generate_token(payload)
    value = token.value
    print("--->>>", value)

    decoded_payload = jwt.decode(value, secret, algorithms=[algorithm])
    print("|||||--->>>", decoded_payload)

    assert isinstance(token, Token)
    assert value
    assert payload == decoded_payload
