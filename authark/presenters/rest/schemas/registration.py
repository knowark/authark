from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RegistrationSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    enroll = fields.Boolean(
        default=False, missing=False)
    organization = fields.Str(
        required=True, metadata=dict(example="Servagro"))
    email = fields.Str(
        required=True, metadata=dict(example="jarango@ops.servagro.com.co"))
    password = fields.Str(
        required=True, metadata=dict(example="secret"))
    username = fields.Str(
        metadata=dict(example="jarango"))
    name = fields.Str(
        metadata=dict(example="Jaime Arango"))
    zone = fields.Str(
        metadata=dict(example="default"))
    attributes = fields.Mapping()
