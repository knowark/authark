from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.yaml_utils import load_yaml_from_docstring
from .schemas import (
    UserSchema, TokenRequestSchema, TokenSchema, AccessTokenPayloadSchema,
    DominionAuthorizationSchema)


def create_spec() -> APISpec:
    spec = APISpec(
        title="Authark",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()],
        info=dict(
            description="Authentication and Authorization Server",
            contact=dict(
                name="Nubark",
                url="https://www.nubark.com"
            )))

    _register_schemas(spec)
    _register_paths(spec)

    return spec


def _register_schemas(spec):
    spec.components.schema("User", schema=UserSchema)
    spec.components.schema("Token", schema=TokenSchema)
    spec.components.schema("TokenRequest", schema=TokenRequestSchema)
    spec.components.schema("DominionAuthorization",
                           schema=DominionAuthorizationSchema)
    spec.components.schema("AccessTokenPayload",
                           schema=AccessTokenPayloadSchema)


def _register_paths(spec):
    spec.path(
        path="/tokens",
        operations={
            'get': {
                'tags': ['Tokens'],
                'responses': _respond("Get all tokens", 'Token')
            }
        }
    ).path(
        path="/users",
        operations={
            'get': {
                'tags': ['Users'],
                'responses': _respond("Get all users", 'User')
            }
        }
    )


def _respond(description, schema, status='200'):
    return {
        status: {
            "description": description,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "$ref": f"#/components/schemas/{schema}"
                        }
                    }
                }
            }
        }
    }
