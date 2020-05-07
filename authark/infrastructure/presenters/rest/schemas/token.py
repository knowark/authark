from marshmallow import Schema, fields


class TokenRequestSchema(Schema):
    tenant = fields.Str(required=True, example="knowark")
    username = fields.Str(example="amlopez")
    password = fields.Str(example="secret")
    refresh_token = fields.Str(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    client = fields.Str(example="data_server")
    dominion = fields.Str(example="platform_xyz")


class TokenSchema(Schema):
    refresh_token = fields.Str(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    access_token = fields.Str(example="eyJhbG.kpvaG4gRMyfQ.SflKxwssw5cdfs")


# class AccessTokenPayloadSchema(Schema):
#     iss = fields.Str(example="authark.nubark.cloud")
#     sub = fields.Str(example="e1fbaebd-6a37-4949-83b3-fb8954b07a2a")
#     iat = fields.Int(example=1543334000)
#     ext = fields.Int(example=1543338055)
#     authorization = fields.Nested('DominionAuthorizationSchema')
