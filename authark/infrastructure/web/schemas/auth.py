from marshmallow import Schema, fields


class PolicySchema(Schema):
    type = fields.Str()
    value = fields.Str()


class ResourceSchema(Schema):
    policies = fields.List()


class DominionSchema(Schema):
    roles = fields.List(fields.Str())
    resources = fields.Dict(
        keys=fields.Str(), values=DominionSchema)


class AuthorizationSchema(Schema):
    dominions = fields.Dict(
        keys=fields.Str(), values=DominionSchema)
