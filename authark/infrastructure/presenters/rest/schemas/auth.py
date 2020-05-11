from marshmallow import Schema, fields


class DominionAuthorizationSchema(Schema):
    roles = fields.List(fields.Str())
