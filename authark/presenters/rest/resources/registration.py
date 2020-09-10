from aiohttp import web
from injectark import Injectark
from ..schemas import RegistrationSchema


class RegistrationResource:
    def __init__(self, injector: Injectark) -> None:
        self.auth_manager = injector['AuthManager']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']

    async def put(self, request: web.Request) -> web.Response:
        registration_dict = RegistrationSchema().loads(await request.text())
        tenant_dict = {
            'name': registration_dict.pop('tenant'),
            'zone': registration_dict.pop('zone'),
            'email': registration_dict['email']}
        self.tenant_supplier.create_tenant(tenant_dict)

        tenant_dict = self.tenant_supplier.resolve_tenant(tenant_dict['name'])
        self.session_manager.set_tenant(tenant_dict)

        await self.auth_manager.register([registration_dict])

        return web.Response(status=200)
