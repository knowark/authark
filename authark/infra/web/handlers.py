from aiohttp import web


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

    resp = {
        "name": "Esteban",
        "proffession": "engineer"
    }

    return web.json_response(resp)
