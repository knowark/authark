import jwt
from authark.app.services.token_service import TokenService
from authark.app.models.token import Token


class PyJWTTokenService(TokenService):

    def generate_token(self) -> Token:
        value = "todo"
        token = Token(value)
        return token
