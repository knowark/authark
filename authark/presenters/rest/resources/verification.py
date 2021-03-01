from aiohttp import web
from injectark import Injectark
from ..schemas import VerificationSchema


class VerificationResource:
    def __init__(self, injector: Injectark) -> None:
        self.auth_manager = injector['AuthManager']
        self.session_manager = injector['SessionManager']
        self.tenant_supplier = injector['TenantSupplier']

    async def put(self, request: web.Request) -> web.Response:
        verification_dict = VerificationSchema().loads(await request.text())

        tenant_dict = self.tenant_supplier.resolve_tenant(
            verification_dict['tenant'])
        self.session_manager.set_tenant(tenant_dict)

        await self.auth_manager.verify([verification_dict])

        return web.Response(status=200)
