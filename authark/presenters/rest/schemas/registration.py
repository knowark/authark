from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RegistrationSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    enroll = fields.Boolean(default=False, missing=False)
    tenant = fields.Str(required=True, metadata=dict(example="knowark"))
    email = fields.Str(
        required=True, metadata=dict(example="jarango@ops.servagro.com.co"))
    username = fields.Str(
        required=True, metadata=dict(example="jarango"))
    password = fields.Str(
        required=True, metadata=dict(example="secret"))
    name = fields.Str(
        required=True, metadata=dict(example="Jaime Arango"))
    zone = fields.Str(metadata=dict(example="default"))
    attributes = fields.Mapping()
