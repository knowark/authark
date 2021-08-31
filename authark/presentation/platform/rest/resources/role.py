from aiohttp import web
from functools import partial
from injectark import Injectark
from ..schemas import RoleSchema
from .resource import Resource
from ..helpers import get_request_filter, get_request_ids


class RoleResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        self.informer = injector['AutharkInformer']
        self.manager = injector['ManagementManager']


    async def head(self, request) -> web.Response:
        domain, _, _ = get_request_filter(request)
        total_count = str(await self.informer.count("role", domain))
        return web.Response(headers={'Total-Count': total_count})

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = get_request_filter(request)
        records = await self.informer.search("role",
            domain, limit=limit, offset=offset)
        result = RoleSchema(many=True).dump(records)
        return web.json_response(result)

    async def put(self, request: web.Request) -> web.Response:
        role_dict = RoleSchema(many=True).loads(await request.text())

        await self.manager.create_role(role_dict)

        return web.Response(status=200)

    async def delete(self, request: web.Request) -> web.Response:
        ids = await get_request_ids(request)
        await self.manager.remove_role(ids)
        return web.Response(status=204)
