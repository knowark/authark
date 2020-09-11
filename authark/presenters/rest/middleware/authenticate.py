from typing import Callable, Dict, Any
from aiohttp import web
from injectark import Injectark
from ....application.managers import SessionManager
from ....core import Config, TenantSupplier


def authenticate_middleware_factory(
        config: Config, injector: Injectark) -> Callable:
    session_coordinator: SessionManager = injector['SessionManager']
    tenant_supplier: TenantSupplier = injector['TenantSupplier']

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        if request.path in ['/', '/registrations', '/tokens']:
            session_coordinator.set_user(config['system'])
            return await handler(request)

        try:
            user_dict = extract_user(request.headers)
            session_coordinator.set_user(user_dict)
            tenant_id = request.headers['TenantId']
            tenant_dict = tenant_supplier.get_tenant(tenant_id)
            session_coordinator.set_tenant(tenant_dict)
        except Exception as error:
            reason = f"{error.__class__.__name__}: {str(error)}"
            raise web.HTTPUnauthorized(reason=reason)
        return await handler(request)

    return middleware


def extract_user(headers: Dict[str, Any]) -> Dict[str, Any]:
    user_id = headers['UserId']
    email = headers.get('From', "@")
    name = email.split('@')[0]
    roles = headers.get('Roles', '').strip().split(',')

    return {
        'id': user_id,
        'name': name,
        'email': email,
        'roles': roles
    }
