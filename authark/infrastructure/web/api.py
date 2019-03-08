from flask import Flask
from ..resolver import Registry
from .resources import RootResource, UserResource, TokenResource
from .spec import create_spec


def create_api(app: Flask, registry: Registry) -> None:

    # Restful API
    spec = create_spec()
    registry['spec'] = spec

    # got_request_exception.connect(log_exception, app)

    # Root Resource (Api Specification)
    root_view = RootResource.as_view('root', registry=registry)
    app.add_url_rule("/", view_func=root_view)

    # Tokens Resource
    token_view = TokenResource.as_view('token', registry=registry)
    app.add_url_rule("/tokens/", view_func=token_view)
    app.add_url_rule("/auth/", view_func=token_view)
    app.add_url_rule("/login/", view_func=token_view)

    # Users Resource
    spec.path(path="/users/", resource=UserResource)
    user_view = UserResource.as_view('user', registry=registry)
    app.add_url_rule("/users/", view_func=user_view)
    app.add_url_rule("/register/", view_func=token_view)
    app.add_url_rule("/signup/", view_func=token_view)
