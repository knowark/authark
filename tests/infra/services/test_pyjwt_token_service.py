from pytest import fixture
from authark.app.models.token import Token
from authark.app.services.token_service import TokenService
from authark.infra.crypto.pyjwt_token_service import PyJWTTokenService


def test_pyjwt_token_service_implementation() -> None:
    assert issubclass(PyJWTTokenService, TokenService)
