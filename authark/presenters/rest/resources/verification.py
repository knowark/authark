from aiohttp import web
from injectark import Injectark
from ..schemas import VerificationSchema


class VerificationResource:
    def __init__(self, injector: Injectark) -> None:
        self.verification_manager = injector['VerificationManager']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']
        setattr(self.put, 'identifier', 'token')

    async def put(self, request: web.Request) -> web.Response:
        token = request.match_info['token']

        verification_dict = VerificationSchema().loads(await request.text())

        tenant_dict = self.tenant_supplier.resolve_tenant(
            verification_dict['organization'])
        self.session_manager.set_tenant(tenant_dict)

        await self.verification_manager.verify(tenant_dict['token'])

        return web.Response(status=200)
