from aiohttp import web
from injectark import Injectark
from ..helpers import get_request_filter


class TenantResource:
    def __init__(self, injector: Injectark) -> None:
        self.tenant_supplier = injector['TenantSupplier']

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = get_request_filter(request)
        tenants = self.tenant_supplier.search_tenants(domain)
        return web.json_response(tenants)
