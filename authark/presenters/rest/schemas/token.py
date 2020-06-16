from marshmallow import Schema, fields


class TokenRequestSchema(Schema):
    tenant = fields.Str(required=True, example="knowark")
    username = fields.Str(example="amlopez")
    password = fields.Str(example="secret")
    refresh_token = fields.Str(data_key='refreshToken',
                               example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    client = fields.Str(example="data_server")
    dominion = fields.Str(example="platform_xyz")


class TokenSchema(Schema):
    refresh_token = fields.Str(
        data_key='refreshToken', example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    access_token = fields.Str(
        data_key='accessToken', example="eyJhbG.kpvaG4gRMyfQ.SflKxwssw5cdfs")
