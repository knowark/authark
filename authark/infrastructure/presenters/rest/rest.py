import aiohttp_cors
import aiohttp_jinja2
from typing import Any
from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web, ClientSession
from injectark import Injectark
from ...core import Config
from .middleware import middlewares
from .doc import create_spec
from .resources import RootResource


class RestApplication(web.Application):
    def __init__(self, config: Config, injector: Injectark) -> None:
        super().__init__(middlewares=middlewares(injector))
        self.config = config
        self.injector = injector
        # self.app = web.Application(middlewares=middlewares(injector))
        self._setup()

    async def run(self, app: web.Application, port=4321) -> None:
        await web._run_app(self, app, port=port)

    def _setup(self) -> None:
        templates = str(Path(__file__).parent / 'templates')
        aiohttp_jinja2.setup(self, loader=FileSystemLoader(templates))

        self.cleanup_ctx.append(self._http_client)
        cors = aiohttp_cors.setup(self, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*",
                allow_headers="*")})

        for route in list(self.router.routes()):
            cors.add(route)

        # API endpoints creation
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
                self.router.add_route(method, path + "/{id}", handler)
            self.router.add_route(method, path, handler)

    def _create_api(self) -> None:
        # Restful API
        spec = create_spec()

        # Resources
        self._bind_routes('/', RootResource(spec))
        # self._bind_routes(self.app, '/processes', ProcessResource(injector))
        # self._bind_routes(self.app, '/triggers', TriggerResource(injector))
