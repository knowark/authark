import json
import aiohttp_jinja2
from typing import Any
from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web, ClientSession
from injectark import Injectark
from .middleware import middlewares
from .resources import (Resource,
    RootResource, TokenResource, TenantResource,
    RegistrationResource, VerificationResource, RequisitionResource)

class RestApplication(web.Application):
    def __init__(self, injector: Injectark) -> None:
        super().__init__(middlewares=middlewares(injector))
        self.injector = injector
        self._setup()

    @staticmethod
    async def run(app: web.Application, port: int = 4321):
        await web._run_app(app, port=port)

    def _setup(self) -> None:
        templates = str(Path(__file__).parent / 'resources')
        aiohttp_jinja2.setup(self, loader=FileSystemLoader(templates))

        self.cleanup_ctx.append(self._http_client)

        spec = json.loads(
            (Path(__file__).parent / 'openapi.json').read_text())

        # Resources
        self.router.add_route(
            "put", '/tokens',
            getattr(TokenResource(self.injector), "put", None))

        # self.router.add_route(
            # "head", '/users',
            # getattr(UserResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/users',
            # getattr(UserResource(self.injector), "get", None))

        # self.router.add_route(
            # "put", '/users',
            # getattr(UserResource(self.injector), "put", None))

        # self.router.add_route(
            # "delete", '/users',
            # getattr(UserResource(self.injector), "delete", None))

        # self.router.add_route(
            # "delete", '/users/{id}',
            # getattr(UserResource(self.injector), "delete", None))

        # self.router.add_route(
            # "head", '/rankings',
            # getattr(RankingResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/rankings',
            # getattr(RankingResource(self.injector), "get", None))

        # self.router.add_route(
            # "put", '/rankings',
            # getattr(RankingResource(self.injector), "put", None))

        # self.router.add_route(
            # "delete", '/rankings',
            # getattr(RankingResource(self.injector), "delete", None))

        # self.router.add_route(
            # "delete", '/rankings/{id}',
            # getattr(RankingResource(self.injector), "delete", None))

        # self.router.add_route(
            # "head", '/dominions',
            # getattr(DominionResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/dominions',
            # getattr(DominionResource(self.injector), "get", None))

        # self.router.add_route(
            # "head", '/roles',
            # getattr(RoleResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/roles',
            # getattr(RoleResource(self.injector), "get", None))

        # self.router.add_route(
            # "put", '/roles',
            # getattr(RoleResource(self.injector), "put", None))

        # self.router.add_route(
            # "delete", '/roles',
            # getattr(RoleResource(self.injector), "delete", None))

        # self.router.add_route(
            # "delete", '/roles/{id}',
            # getattr(RoleResource(self.injector), "delete", None))

        # self.router.add_route(
            # "head", '/policies',
            # getattr(PolicyResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/policies',
            # getattr(PolicyResource(self.injector), "get", None))

        # self.router.add_route(
            # "put", '/policies',
            # getattr(PolicyResource(self.injector), "put", None))

        # self.router.add_route(
            # "delete", '/policies',
            # getattr(PolicyResource(self.injector), "delete", None))

        # self.router.add_route(
            # "delete", '/policies/{id}',
            # getattr(PolicyResource(self.injector), "delete", None))

        # self.router.add_route(
            # "head", '/restrictions',
            # getattr(RestrictionResource(self.injector), "head", None))

        # self.router.add_route(
            # "get", '/restrictions',
            # getattr(RestrictionResource(self.injector), "get", None))

        # self.router.add_route(
            # "put", '/restrictions',
            # getattr(RestrictionResource(self.injector), "put", None))

        # self.router.add_route(
            # "delete", '/restrictions',
            # getattr(RestrictionResource(self.injector), "delete", None))

        # self.router.add_route(
            # "delete", '/restrictions/{id}',
            # getattr(RestrictionResource(self.injector), "delete", None))

        self.router.add_route(
            "get", '/tenants',
            getattr(TenantResource(self.injector), "get", None))

        self.router.add_route(
            "put", '/registrations',
            getattr(RegistrationResource(self.injector), "put", None))

        self.router.add_route(
            "put", '/verifications',
            getattr(VerificationResource(self.injector), "put", None))

        self.router.add_route(
            "put", '/requisitions',
            getattr(RequisitionResource(self.injector), "put", None))

        self._create_api(spec)

    @staticmethod
    async def _http_client(app: web.Application):
        session = ClientSession()
        app['client'] = session
        yield
        await session.close()

    def _create_api(self, spec) -> None:

        resource = Resource(spec, self.injector)
        self.add_routes([
            web.get('/', RootResource(spec).get),

            web.get('/{resource}/{id}', resource.get, allow_head=False),
            web.get('/{resource}', resource.get, allow_head=False),

            web.head('/{resource}/{id}', resource.head),
            web.head('/{resource}', resource.head),

            web.patch('/{resource}/{id}', resource.patch),
            web.patch('/{resource}', resource.patch),

            web.delete('/{resource}/{id}', resource.delete),
            web.delete('/{resource}', resource.delete)
        ])
