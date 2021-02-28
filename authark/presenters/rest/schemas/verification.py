from marshmallow import fields, EXCLUDE
from .entity import EntitySchema


class VerificationSchema(EntitySchema):
    class Meta:
        unknown = EXCLUDE

    organization = fields.Str(
        required=True, metadata=dict(example="Servagro"))
    token = fields.Str(
        required=True, metadata=dict(
            example=("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM"
                     "0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM"
                     "5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")))
