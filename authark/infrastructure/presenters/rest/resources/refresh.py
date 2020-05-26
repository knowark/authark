# from typing import Any, Dict, Tuple

from aiohttp import web
from injectark import Injectark
from ..schemas import RefreshRequestSchema, RefreshSchema


class RefreshResource:
    def __init__(self, injector: Injectark) -> None:
        self.auth_manager = injector['AuthManager']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']

    async def put(self, request: web.Request) -> web.Response:
        token_request = RefreshRequestSchema().loads(await request.text())
        tenant_id = token_request['tenant']
        tenant_dict = self.tenant_supplier.resolve_tenant(tenant_id)
        self.session_manager.set_tenant(tenant_dict)
        token_pair = await self.auth_manager.authenticate(token_request)
        return web.json_response(RefreshSchema().dump(token_pair))