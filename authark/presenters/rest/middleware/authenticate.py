import jwt
from typing import Callable, Dict, Any
from aiohttp import web
from injectark import Injectark
from ....application.managers import SessionManager
from ....core import Config, TenantSupplier


def authenticate_middleware_factory(
        config: Config, injector: Injectark) -> Callable:
    session_manager: SessionManager = injector['SessionManager']
    secret = injector.config['tokens']['rest']['secret']

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        public = ['/', '/tenants', '/registrations',
                  '/verifications', '/requisitions', '/tokens']
        if request.path in public:
            session_manager.set_user({'meta': {'anonymous': True}})
            return await handler(request)

        token = request.headers.get(
            'Authorization', '').replace('Bearer ', '')
        token = token or request.query.get('access_token', '')

        try:
            payload = jwt.decode(
                token, secret, algorithms=['HS256'],
                options={"verify_signature": bool(secret)})

            session_manager.set_user(payload)

        except Exception as error:
            reason = f"{error.__class__.__name__}: {str(error)}"
            raise web.HTTPUnauthorized(reason=reason)
        return await handler(request)

    return middleware
