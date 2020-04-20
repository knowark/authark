import jwt
import time
from pytest import fixture, raises
from authark.application.models import Token
from authark.application.services import TokenService
from authark.infrastructure.core import PyJWTTokenService
from authark.infrastructure.core.crypto import pyjwt_token_service


def test_pyjwt_token_service_implementation() -> None:
    assert issubclass(PyJWTTokenService, TokenService)


def test_pyjwt_token_service_generate_token_with_payload(pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    expiration = 1539715900
    payload = {'user': "Pepe", 'email': "pepe@gmail.com", 'exp': expiration}

    token = pyjwt_service.generate_token(payload)
    value = token.value

    decoded_payload = jwt.decode(value, secret, algorithms=[algorithm])

    assert isinstance(token, Token)
    assert value
    assert payload == decoded_payload


def test_pyjwt_token_service_renew_false_no_threshold(pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'user': "Pepe", 'email': "pepe@gmail.com", 'exp': 1539715900}

    value = jwt.encode(payload, secret, algorithm=algorithm)
    token = Token(str(value, 'utf-8'))

    pyjwt_service.threshold = None

    result = pyjwt_service.renew(token)

    assert result is False


def test_pyjwt_token_service_renew_true(monkeypatch, pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'exp': 1539715900}

    value = jwt.encode(payload, secret, algorithm=algorithm)
    token = Token(str(value, 'utf-8'))

    monkeypatch.setattr(
        pyjwt_token_service, "time", lambda: 1539715900 - 30)

    monkeypatch.setattr(
        pyjwt_token_service.jwt.PyJWT, "_validate_exp",
        lambda self, payload, now, leeway: None)

    result = pyjwt_service.renew(token)
    assert result is True


def test_pyjwt_token_service_renew_false_too_early(
        monkeypatch, pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'exp': 1539715900}

    value = jwt.encode(payload, secret, algorithm=algorithm)
    token = Token(str(value, 'utf-8'))

    monkeypatch.setattr(
        pyjwt_token_service, "time", lambda: 1539715900 - 90)

    monkeypatch.setattr(
        pyjwt_token_service.jwt.PyJWT, "_validate_exp",
        lambda self, payload, now, leeway: None)

    result = pyjwt_service.renew(token)
    assert result is False


def test_pyjwt_token_service_valid_true(
        monkeypatch, pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'exp': 1539715900}

    value = jwt.encode(payload, secret, algorithm=algorithm)
    token = Token(str(value, 'utf-8'))

    # Bypass the expiration validation
    monkeypatch.setattr(
        pyjwt_token_service.jwt.PyJWT, "_validate_exp",
        lambda self, payload, now, leeway: None)

    result = pyjwt_service.valid(token)
    assert result is True


def test_pyjwt_token_service_invalid(
        monkeypatch, pyjwt_service):
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    payload = {'exp': 0}

    value = jwt.encode(payload, secret, algorithm=algorithm)
    token = Token(str(value, 'utf-8'))

    with raises(jwt.ExpiredSignature):
        pyjwt_service.valid(token)
