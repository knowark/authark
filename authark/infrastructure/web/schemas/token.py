from marshmallow import Schema, fields


class TokenRequestSchema(Schema):
    tenant = fields.Email(required=True, example="knowark")
    username = fields.Str(example="amlopez")
    password = fields.Email(example="secret")
    refresh_token = fields.Str(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    client = fields.Str(example="data_server")


class TokenSchema(Schema):
    refresh_token = fields.Str(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    access_token = fields.Email(example="eyJhbG.kpvaG4gRMyfQ.SflKxwssw5cdfs")


class AccessTokenPayloadSchema(Schema):
    iss = fields.Str(example="authark.nubark.cloud")
    sub = fields.Str(example="e1fbaebd-6a37-4949-83b3-fb8954b07a2a")
    iat = fields.Int(example=1543334000)
    ext = fields.Int(example=1543338055)
    authorization = fields.Nested('DominionAuthorizationSchema')
