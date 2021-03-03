from aiohttp import web
from injectark import Injectark
from ..schemas import RequisitionSchema


class RequisitionResource:
    def __init__(self, injector: Injectark) -> None:
        self.procedure_manager = injector['ProcedureManager']
        self.session_manager = injector['SessionManager']
        self.tenant_supplier = injector['TenantSupplier']

    async def put(self, request: web.Request) -> web.Response:
        requisition_dict = RequisitionSchema().loads(await request.text())

        tenant_dict = self.tenant_supplier.resolve_tenant(
            requisition_dict['tenant'])
        self.session_manager.set_tenant(tenant_dict)

        await self.procedure_manager.fulfill([requisition_dict])

        return web.Response(status=200)
