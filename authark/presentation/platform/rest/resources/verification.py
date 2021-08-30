from aiohttp import web
from injectark import Injectark
from ..schemas import VerificationSchema


class VerificationResource:
    def __init__(self, injector: Injectark) -> None:
        self.procedure_manager = injector['ProcedureManager']

    async def put(self, request: web.Request) -> web.Response:
        verification_dict = VerificationSchema().loads(await request.text())

        await self.procedure_manager.verify([verification_dict])

        return web.Response(status=200)
