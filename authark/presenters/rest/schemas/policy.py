from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class PolicySchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(
        required=True, example="1a915516-3875-44f6-ae96-7eea2e7d7981")
    resource = fields.Str(required=True, example="Name resource")
    privilege = fields.Str(required=True, example="Name privilege")
    role_id = fields.Str(data_key='roleId', required=True,
                         example="e9fa671b-1124-4c8e-9041-40c4d1986df2")
    restriction = fields.Str(required=True, example="Name restriction")
