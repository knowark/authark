from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RuleSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(example="1a915516-3875-44f6-ae96-7eea2e7d7981")
    group = fields.Str(required=True, example="Name Group")
    sequence = fields.Str(required=True, example="1")
    target = fields.Str(required=True, example="Name Target")
    domain = fields.Str(required=True, example="domain")
    name = fields.Str(required=True, example="name rule")
