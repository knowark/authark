from flask import Flask, jsonify
from injectark import Injectark
from .resources import RootResource, UserResource, TokenResource
from .spec import create_spec


def create_api(app: Flask, resolver: Injectark) -> None:

    # Restful API
    spec = create_spec()

    # Root Resource (Api Specification)
    root_view = RootResource.as_view('root', spec=spec)
    app.add_url_rule("/", view_func=root_view)

    # Middleware
    authenticate = resolver.resolve('Authenticate')

    # Tokens Resource
    spec.path(path="/tokens", resource=TokenResource)
    token_view = TokenResource.as_view('token', resolver=resolver)
    app.add_url_rule("/tokens", view_func=token_view)
    app.add_url_rule("/auth", view_func=token_view)
    app.add_url_rule("/login", view_func=token_view)

    # Users Resource
    spec.path(path="/users", resource=UserResource)
    user_view = authenticate(
        UserResource.as_view('user', resolver=resolver))
    app.add_url_rule("/users", view_func=user_view)
    app.add_url_rule("/register", view_func=user_view)
    app.add_url_rule("/signup", view_func=user_view)
