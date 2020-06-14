import jwt
from authark.core import PyJWTTokenService


def test_pyjwt_token_service_instantiation(pyjwt_service):
    assert isinstance(pyjwt_service, PyJWTTokenService)


def test_pyjwt_token_service_generate_token(pyjwt_service):
    payload = {'name': 'john', 'code': '5432'}
    token = pyjwt_service.generate_token(payload)
    decoded_payload = jwt.decode(
        token.value, pyjwt_service.secret,
        algorithms=[pyjwt_service.algorithm])
    assert decoded_payload == decoded_payload


def test_pyjwt_token_service_valid(pyjwt_service):
    payload = {'name': 'john', 'code': '5432'}
    token = pyjwt_service.generate_token(payload)
    assert pyjwt_service.valid(token) is True
