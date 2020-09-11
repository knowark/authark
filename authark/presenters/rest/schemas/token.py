from marshmallow import Schema, fields


class TokenRequestSchema(Schema):
    dominion = fields.Str(required=True, example="platform_xyz")
    tenant = fields.Str(required=True, example="knowark")
    username = fields.Str(example="amlopez")
    password = fields.Str(example="secret")
    refresh_token = fields.Str(data_key='refreshToken',
                               example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    client = fields.Str(example="data_server")


class TokenSchema(Schema):
    refresh_token = fields.Str(
        data_key='refreshToken', example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c")
    access_token = fields.Str(
        data_key='accessToken', example="eyJhbG.kpvaG4gRMyfQ.SflKxwssw5cdfs")
