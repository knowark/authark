from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class PolicySchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    resource = fields.Str(
        required=True, metadata=dict(example="Name resource"))
    role_id = fields.Str(
        data_key='roleId', required=True,
        metadata=dict(example="e9fa671b-1124-4c8e-9041-40c4d1986df2"))
    privilege = fields.Str(
        required=True, metadata=dict(example="Name privilege"))
    active = fields.Bool(
        required=True, metadata=dict(example="True"))
