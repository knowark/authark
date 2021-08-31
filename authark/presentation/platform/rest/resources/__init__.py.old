from aiohttp import web
from ..... import __version__
from .token import TokenResource
from .resource import Resource
from .user import UserResource
from .dominion import DominionResource
from .restriction import RestrictionResource
from .policy import PolicyResource
from .ranking import RankingResource
from .registration import RegistrationResource
from .tenant import TenantResource
from .verification import VerificationResource
from .requisition import RequisitionResource
from .role import RoleResource


class RootResource:

    def __init__(self, app, spec) -> None:
        self.app = app
        self.spec = spec

    async def get(self, request: web.Request) -> web.Response:
        if 'api' in request.query:
            return web.json_response(self.spec.to_dict())

        context = {'url': '/?api', 'version': __version__}
        template = self.app['jinja'].get_template('index.html')

        response = web.Response(text=template.render(context))
        response.headers['Content-Type'] = 'text/html'

        return response
