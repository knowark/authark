from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from .schemas import (
    UserSchema, TokenRequestSchema, TokenSchema, DominionSchema,
    RoleSchema, RestrictionSchema, PolicySchema, RankingSchema)


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
    spec.components.schema("Dominion", schema=DominionSchema)
    spec.components.schema("Role", schema=RoleSchema)
    spec.components.schema("Ranking", schema=RankingSchema)
    spec.components.schema("Policy", schema=PolicySchema)
    spec.components.schema("Restriction", schema=RestrictionSchema)


def _register_paths(spec):
    resources = [
        ('tokens', 'Token'),
        ('users', 'User'),
        ('dominions', 'Dominion'),
        ('roles', 'Role'),
        ('restrictions', 'Restriction'),
        ('policies', 'Policy'),
        ('rankings', 'Ranking'),
        ('sites', 'Site'),
        ('traces', 'Trace'),
        ('users', 'User'),
    ]
    for resource in resources:
        _append_path(spec, *resource)


def _append_path(spec, endpoint, schema):
    spec.path(
        path=f'/{endpoint}',
        operations={
            'get': {
                'tags': [schema],
                'responses': _respond(f"Get all {endpoint}", schema)
            },
            'put': {
                'tags': [schema],
                'responses': _respond(f"Modify {endpoint}", schema)
            },
            'delete': {
                'tags': [schema],
                'responses': _respond(f"Delete {endpoint}", schema)
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
