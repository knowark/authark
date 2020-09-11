from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class UserSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(example="Jaime Arango")
    email = fields.Str(example="jarango@ops.servagro.com.co")
    username = fields.Str(example="jarango")
    password = fields.Str(load_only=True, example="secret")
    attributes = fields.Mapping()
