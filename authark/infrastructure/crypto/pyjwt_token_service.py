import jwt
from time import time
from typing import Dict, Any
from authark.application.services.token_service import TokenService
from authark.application.models.token import Token


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
        token = Token(str(value, 'utf-8'))
        return token

    def valid(self, token: Token) -> bool:
        decoded_payload = jwt.decode(
            token.value, self.secret, algorithms=[self.algorithm])
        return True

    def renew(self, token: Token) -> bool:
        if self.threshold is None:
            return False

        decoded_payload = jwt.decode(
            token.value, self.secret, algorithms=[self.algorithm])
        expiration = decoded_payload.get('exp', -1)
        now = time()

        if expiration - self.threshold <= now <= expiration:
            return True

        return False
