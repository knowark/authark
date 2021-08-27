from aiohttp import web
from injectark import Injectark
from ..schemas import TokenRequestSchema, TokenSchema


class TokenResource:
    def __init__(self, injector: Injectark) -> None:
        self.auth_manager = injector['AuthManager']

    async def put(self, request: web.Request) -> web.Response:
        token_request = TokenRequestSchema().loads(await request.text())

        token_pair = await self.auth_manager.authenticate(token_request)

        return web.json_response(TokenSchema().dump(token_pair))
