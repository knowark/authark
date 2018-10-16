import jwt
from time import time
from typing import Dict, Any
from authark.application.services.token_service import TokenService
from authark.application.models.token import Token


class PyJWTTokenService(TokenService):

    def __init__(self, secret: str, algorithm: str, lifetime: int) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.lifetime = lifetime

    def generate_token(self, payload: Dict[str, Any]) -> Token:
        payload = payload or {}
        payload['exp'] = int(time()) + int(self.lifetime)
        value = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        token = Token(str(value, 'utf-8'))
        return token
