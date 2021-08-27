from aiohttp import web
from injectark import Injectark
from ..schemas import RequisitionSchema


class RequisitionResource:
    def __init__(self, injector: Injectark) -> None:
        self.procedure_manager = injector['ProcedureManager']

    async def put(self, request: web.Request) -> web.Response:
        requisition_dict = RequisitionSchema().loads(await request.text())

        await self.procedure_manager.fulfill([requisition_dict])

        return web.Response(status=200)
