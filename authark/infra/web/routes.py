from aiohttp import web
import authark.infra.web.handlers as handlers
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.infra.db.memory_user_repository import MemoryUserRepository
from authark.infra.web.controllers import AuthController


def set_routes(app: web.Application) -> None:
    app.router.add_route('GET', '/', handlers.handle)

    login_resource = app.router.add_resource('/login', name='login')
    login_resource.add_route('GET', handlers.login)
    login_resource.add_route('POST', handlers.login)

    # Auth resource
    user_repository = MemoryUserRepository()
    auth_coordinator = AuthCoordinator(user_repository)
    auth_controller = AuthController(auth_coordinator)

    auth_resource = app.router.add_resource('/auth', name='auth')
    auth_resource.add_route('POST', auth_controller.authenticate)
