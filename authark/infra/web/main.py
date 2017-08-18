from aiohttp import web
import infra.web.routes as routes


app = web.Application()
routes.set_routes(app)


def main() -> None:
    web.run_app(app)
