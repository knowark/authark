from aiohttp import web
from authark.app.coordinators.auth_coordinator import AuthCoordinator


class AuthController:

    def __init__(self, auth_coordinator: AuthCoordinator) -> None:
        pass

    async def authenticate(self, request: web.Request) -> web.Response:
        name = request.match_info.get('name', "Anonymous")

        params = await request.json()
        print("On authenticate!!!")
        print("--->>>", params)
        if not params:
            return web.Response()

        name = params.get("username")
        password = params.get("password")

        txt = "Hello, {}".format(name)
        return web.Response(text=txt)
