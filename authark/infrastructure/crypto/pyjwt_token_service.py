from typing import Dict
import jwt
from authark.application.services.token_service import TokenService
from authark.application.models.token import Token


class PyJWTTokenService(TokenService):

    def __init__(self, secret: str, algorithm: str) -> None:
        self.secret = secret
        self.algorithm = algorithm

    def generate_token(self, payload: Dict[str, str]) -> Token:
        payload = payload or {}
        value = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        token = Token(str(value, 'utf-8'))
        return token
