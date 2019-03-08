from flask import Flask
from flask_restful import Api
# from flasgger import Swagger
from apispec import APISpec
from ..resolver import Registry
from .resources import RootResource, UserResource, TokenResource


def create_api(app: Flask, registry: Registry) -> None:

    # Restful API
    api = Api(app)

    # Swagger
    # Swagger(app, template_file="api.yml", config={
    #     "specs_route": "/",
    #     "headers": [],
    #     "specs": [{
    #         "endpoint": 'apispec_1',
    #         "route": '/apispec_1.json',
    #         "rule_filter": lambda rule: True,
    #         "model_filter": lambda tag: True,
    #     }],
    #     "static_url_path": "/flasgger_static",
    #     "swagger_ui": True
    # })

    spec = APISpec(
        title="Authark",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="Authentication and Authorization Server"))

    registry['spec'] = spec

    api.add_resource(
        RootResource, '/', resource_class_kwargs=registry)

    # Tokens Resource
    api.add_resource(
        TokenResource,
        '/auth', '/login', '/tokens',
        resource_class_kwargs=registry)

    # Users Resource
    api.add_resource(
        UserResource,
        '/register', '/signup', '/users',
        resource_class_kwargs=registry)
