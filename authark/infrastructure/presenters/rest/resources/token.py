# from typing import Any, Dict, Tuple
from ..schemas import TokenRequestSchema, TokenSchema

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
        tenant_id = token_request['tenant']
        tenant_dict = self.tenant_supplier.get_tenant(tenant_id)
        self.session_manager.set_tenant(tenant_dict)

        token_pair = await self.auth_manager.authenticate(token_request)
        return web.json_response(TokenSchema().dump(token_pair))


# class TokenResourcex:

#     def __init__(self, resolver) -> None:
#         self.session_coordinator = resolver['SessionCoordinator']
#         self.auth_coordinator = resolver['AuthCoordinator']
#         self.tenant_supplier = resolver['TenantSupplier']

#     def get(self) -> str:
#         return "Authentication endpoint. Please 'Post' to '/auth'"

#     def post(self) -> None:
#         """
#         ---
#         summary: Request token.
#         tags:
#           - Tokens
#         requestBody:
#           required: true
#           content:
#             application/json:
#               schema:
#                 $ref: '#/components/schemas/TokenRequest'
#         responses:
#           201:
#             description: "Token created"
#             content:
#               application/json:
#                 schema:
#                   $ref: "#/components/schemas/Token"
#         """
#         # data = str(request.data, encoding='utf8')
#         # token_request_dict = TokenRequestSchema().loads(data)
#         # tenant_name = token_request_dict['tenant']
#         # tenants = self.tenant_supplier.search_tenants(
#         #     [('slug', '=', tenant_name)])
#         # dominion = token_request_dict.get('dominion')

#         # self.session_coordinator.set_tenant(tenants[0])

#         # if 'refresh_token' in token_request_dict:
#         #     tokens = self.auth_coordinator.refresh_authenticate(
#         #         token_request_dict['refresh_token'], dominion)
#         # else:
#         #     username = token_request_dict.get('username')
#         #     password = token_request_dict.get('password')
#         #     client = token_request_dict.get('client')
#         #     tokens = self.auth_coordinator.authenticate(
#         #         username, password, client, dominion)

#         # tokens_dict = TokenSchema().load(tokens)

#         # return jsonify(tokens_dict), 200
#         pass
