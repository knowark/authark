from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RestrictionSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    group = fields.Str(required=True, example="Name Group")
    sequence = fields.Str(required=True, example="1")
    target = fields.Str(required=True, example="Name Target")
    domain = fields.Str(required=True, example="domain")
    name = fields.Str(required=True, example="name restriction")
