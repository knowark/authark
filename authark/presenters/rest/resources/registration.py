from aiohttp import web
from injectark import Injectark
from ..schemas import RegistrationSchema


class RegistrationResource:
    def __init__(self, injector: Injectark) -> None:
        self.procedure_manager = injector['ProcedureManager']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']

    async def put(self, request: web.Request) -> web.Response:
        registration_dict = RegistrationSchema().loads(await request.text())

        await self.procedure_manager.register([registration_dict])

        return web.Response(status=200)
