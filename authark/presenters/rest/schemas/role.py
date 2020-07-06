from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RoleSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, example="Role name")
    description = fields.Str(required=True, example="Description")
    dominion_id = fields.Str(data_key='dominionId', required=True,
                             example="8f8eb939-6891-4d16-a705-9bc37c053d5d")
