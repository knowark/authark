from aiohttp import web
from app.models.user import User


async def handle(request: web.Request) -> web.Response:
    text = "Welcome to Authark!"
    return web.Response(text=text)


users = {
    "john": "hello",
    "susan": "bye"
}


async def login(request: web.Request) -> web.Response:
    print("method:", request.method)
    if request.method != 'POST':
        print("Try using post...")
        return web.json_response({})

    params = await request.json()
    user = User(name="Esteban EP", email="abc@xyz.com")
    user = params.get('username', None)
    password = params.get('password', None)
    print("user:", user)
    print("password:", password)

    resp = {
        "name": "Esteban",
        "proffession": "engineer"
    }

    return web.json_response(resp)
