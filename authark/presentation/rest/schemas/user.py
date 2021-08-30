from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class UserSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(metadata=dict(example="Jaime Arango"))
    email = fields.Str(metadata=dict(example="jarango@ops.servagro.com.co"))
    username = fields.Str(metadata=dict(example="jarango"))
    password = fields.Str(
        load_only=True, metadata=dict(example="secret"))
    attributes = fields.Mapping()
