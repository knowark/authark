from aiohttp import web
from injectark import Injectark
from ..helpers import get_request_filter


class TenantResource:
    def __init__(self, injector: Injectark) -> None:
        #self.tenant_supplier = injector['TenantSupplier']
        self.tenant_informer = injector['TenantInformer']

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = get_request_filter(request)
        #tenants = self.tenant_supplier.search_tenants(domain)
        tenants = await self.tenant_informer.search_tenants({
            "meta":{
                "domain":domain
            }
        })
        return web.json_response(tenants)
