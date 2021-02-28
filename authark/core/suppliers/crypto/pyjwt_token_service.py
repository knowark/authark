import jwt
from time import time
from typing import Dict, Any
from ....application.domain.models import Token
from ....application.domain.services import (
    TokenService, AccessTokenService, RefreshTokenService,
    VerificationTokenService)


class PyJWTTokenService(TokenService):

    def __init__(self, secret: str, algorithm: str, lifetime: int,
                 threshold: int = None) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.lifetime = lifetime
        self.threshold = threshold

    def generate_token(self, payload: Dict[str, Any]) -> Token:
        payload = payload or {}
        payload['exp'] = int(time()) + int(self.lifetime)
        value = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        token = Token(value)
        return token

    def valid(self, token: Token) -> bool:
        jwt.decode(token.value, self.secret,
                   algorithms=[self.algorithm])
        return True


class PyJWTAccessTokenService(PyJWTTokenService, AccessTokenService):
    """PyJWT Access Token Service"""


class PyJWTRefreshTokenService(PyJWTTokenService, RefreshTokenService):
    """PyJWT Refresh Token Service"""


class PyJWTVerificationTokenService(
        PyJWTTokenService, VerificationTokenService):
    """PyJWT Verification Token Service"""
