from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class RankingSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, example="1a915516-3875-44f6-ae96-7eea2e7d7981")
    user_id = fields.Str(data_key='userId', required=True, example="f52706c8-ac08-4f9d-a092-8038d1769821")
    role_id = fields.Str(data_key='roleId', required=True, example="001")
