from typing import Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from aiohttp import web, ClientSession
from injectark import Injectark
from ...core import Config
from .middleware import middlewares
from .doc import create_spec
from .resources import (
    RootResource, UserResource, TokenResource, DominionResource, RoleResource,
    RestrictionResource, PolicyResource, RankingResource, TenantResource,
    RegistrationResource, VerificationResource, RequisitionResource)


class RestApplication:
    def __init__(self, config: Config, injector: Injectark) -> None:
        super().__init__()
        self.app = web.Application(middlewares=middlewares(config, injector))
        self.config = config
        self.injector = injector
        self._setup()

    @staticmethod
    async def run(rest: 'RestApplication', port: int = 4321):
        await web._run_app(rest.app, port=port)

    def _setup(self) -> None:
        templates = str(Path(__file__).parent / 'templates')
        self.app['jinja'] = Environment(loader=FileSystemLoader(templates))
        self.app.cleanup_ctx.append(self._http_client)
        self._create_api()

    @staticmethod
    async def _http_client(app: web.Application):
        session = ClientSession()
        app['client'] = session
        yield
        await session.close()

    def _bind_routes(self, path: str, resource: Any):
        general_methods = ['head', 'get', 'put', 'delete', 'post', 'patch']
        identified_methods = ['get', 'delete']
        for method in general_methods + identified_methods:
            handler = getattr(resource, method, None)
            if not handler:
                continue
            if method in identified_methods:
                self.app.router.add_route(method, path + "/{id}", handler)
            self.app.router.add_route(method, path, handler)

    def _create_api(self) -> None:
        # Restful API
        spec = create_spec()

        # Resources
        self._bind_routes('/', RootResource(self.app, spec))
        self._bind_routes('/tokens', TokenResource(self.injector))
        self._bind_routes('/users', UserResource(self.injector))
        self._bind_routes('/rankings', RankingResource(self.injector))
        self._bind_routes('/dominions', DominionResource(self.injector))
        self._bind_routes('/roles', RoleResource(self.injector))
        self._bind_routes('/policies', PolicyResource(self.injector))
        self._bind_routes('/restrictions', RestrictionResource(self.injector))
        self._bind_routes('/tenants', TenantResource(self.injector))
        self._bind_routes(
            '/registrations', RegistrationResource(self.injector))
        self._bind_routes(
            '/verifications', VerificationResource(self.injector))
        self._bind_routes(
            '/requisitions', RequisitionResource(self.injector))
