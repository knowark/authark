from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RestrictionSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    policy_id = fields.Str(
        data_key='policyId', required=True,
        metadata=dict(example="e6d17f7c-a2a2-4670-ba0d-ff66d4acd4a4"))
    sequence = fields.Str(
        required=True, metadata=dict(example="1"))
    name = fields.Str(
        required=True, metadata=dict(example="Restriction name"))
    target = fields.Str(
        required=True, metadata=dict(example="Name resource"))
    domain = fields.Str(
        required=True, metadata=dict(example="[['user_id', '=', '123']]"))
