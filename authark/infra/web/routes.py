from aiohttp import web
import infra.web.handlers as handlers


def set_routes(app: web.Application) -> None:
    app.router.add_route('GET', '/', handlers.handle)

    login_resource = app.router.add_resource('/login', name='login')
    login_resource.add_route('GET', handlers.login)
    login_resource.add_route('POST', handlers.login)
