from json import loads
from aiohttp import web
from functools import partial
from injectark import Injectark
from ..schemas import UserSchema
from .resource import Resource
from ..helpers import get_request_filter, get_request_ids


class UserResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        self.informer = injector['AutharkInformer']
        self.manager = injector['ProcedureManager']


    async def head(self, request) -> web.Response:
        domain, _, _ = get_request_filter(request)
        total_count = str(await self.informer.count("user",domain))
        return web.Response(headers={'Total-Count': total_count})

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = get_request_filter(request)
        records = await self.informer.search("user",
            domain, limit=limit, offset=offset)
        result = UserSchema(many=True).dump(records)
        return web.json_response(result)

    async def put(self, request: web.Request) -> web.Response:
        user_dict = UserSchema(many=True).loads(await request.text())
        await self.manager.update(user_dict)

        return web.Response(status=200)

    async def delete(self, request: web.Request) -> web.Response:
        ids = await get_request_ids(request)
        await self.manager.deregister(ids)
        return web.Response(status=204)
