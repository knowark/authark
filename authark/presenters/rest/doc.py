from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from .schemas import (
    UserSchema, TokenRequestSchema, TokenSchema, RoleSchema,
    RestrictionSchema, PolicySchema, RankingSchema)


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
    spec.components.schema("Role", schema=RoleSchema)
    spec.components.schema("Ranking", schema=RankingSchema)
    spec.components.schema("Policy", schema=PolicySchema)
    spec.components.schema("Restriction", schema=RestrictionSchema)


def _register_paths(spec):
    spec.path(
        path="/tokens",
        operations={
            'put': {
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
            },
            'put': {
                'tags': ['Users'],
                'responses': _respond("Modify users", 'Users')
            },
            'delete': {
                'tags': ['Users'],
                'responses': _respond("Delete users", 'Users')
            }
        }
    ).path(
        path="/roles",
        operations={
            'get': {
                'tags': ['Roles'],
                'responses': _respond("Get all roles", 'Roles')
            },
            'put': {
                'tags': ['Roles'],
                'responses': _respond("Modify roles", 'Roles')
            },
            'delete': {
                'tags': ['Roles'],
                'responses': _respond("Delete roles", 'Roles')
            }
        }
    ).path(
        path="/restrictions",
        operations={
            'get': {
                'tags': ['Restrictions'],
                'responses': _respond("Get all restrictions", 'Restrictions')
            },
            'put': {
                'tags': ['Restrictions'],
                'responses': _respond("Modify restrictions", 'Restrictions')
            },
            'delete': {
                'tags': ['Restrictions'],
                'responses': _respond("Delete restrictions", 'Restrictions')
            }
        }
    ).path(
        path="/policies",
        operations={
            'get': {
                'tags': ['Policies'],
                'responses': _respond("Get all policies", 'Policies')
            },
            'put': {
                'tags': ['Policies'],
                'responses': _respond("Modify policies", 'Policies')
            },
            'delete': {
                'tags': ['Policies'],
                'responses': _respond("Delete policies", 'Policies')
            }
        }
    ).path(
        path="/rankings",
        operations={
            'get': {
                'tags': ['Rankings'],
                'responses': _respond("Get all rankings", 'Rankings')
            },
            'put': {
                'tags': ['Rankings'],
                'responses': _respond("Modify rankings", 'Rankings')
            },
            'delete': {
                'tags': ['Rankings'],
                'responses': _respond("Delete rankings", 'Rankings')
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
