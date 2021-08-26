from aiohttp import web
from injectark import Injectark
from ..schemas import TokenRequestSchema, TokenSchema


class TokenResource:
    def __init__(self, injector: Injectark) -> None:
        self.auth_manager = injector['AuthManager']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']

    async def put(self, request: web.Request) -> web.Response:
        token_request = TokenRequestSchema().loads(await request.text())
        # tenant = token_request['tenant']
        # token_request['dominion'] = token_request.get(
            # 'dominion', request.headers.get('Dominion', ''))
        # tenant_dict = self.tenant_supplier.resolve_tenant(tenant)
        # self.session_manager.set_tenant(tenant_dict)

        token_pair = await self.auth_manager.authenticate(token_request)
        return web.json_response(TokenSchema().dump(token_pair))
