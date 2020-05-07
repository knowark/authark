from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class UserSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    tenant = fields.Str(required=True, load_only=True, example="knowark")
    password = fields.Str(required=True, load_only=True, example="secret")
    username = fields.Str(example="jarango")
    email = fields.Str(example="jarango@ops.servagro.com.co")
    name = fields.Str(example="Jaime Arango")
    attributes = fields.Mapping()
