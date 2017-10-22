from typing import Dict
import jwt
from authark.app.services.token_service import TokenService
from authark.app.models.token import Token


class PyJWTTokenService(TokenService):

    def __init__(self, payload: Dict[str, str], secret: str,
                 algorithm: str) -> None:
        self.payload = payload
        self.secret = secret
        self.algorithm = algorithm

    def generate_token(self) -> Token:
        payload = self.payload or {}
        value = jwt.encode(self.payload, self.secret, algorithm=self.algorithm)
        token = Token(value)
        return token
