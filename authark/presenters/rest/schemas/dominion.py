from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class DominionSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, metadata=dict(example="cloudplatform"))
