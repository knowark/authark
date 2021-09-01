from aiohttp import web
from functools import partial
from injectark import Injectark
from ..schemas import DominionSchema
#from ..helpers import missing
from .resource import Resource
from ..helpers import get_request_filter, get_request_ids


class DominionResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        self.informer = injector['AutharkInformer']

    async def head(self, request) -> web.Response:
        domain, _, _ = get_request_filter(request)
        total_count = str(await self.informer.count("dominion", domain))
        return web.Response(headers={'Total-Count': total_count})

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = get_request_filter(request)
        records = await self.informer.search("dominion",
            domain, limit=limit, offset=offset)
        result = DominionSchema(many=True).dump(records)
        return web.json_response(result)
