from marshmallow import Schema, fields


class TokenRequestSchema(Schema):
    dominion = fields.Str(
        metadata=dict(example="platform_xyz"))
    tenant = fields.Str(
        required=True, metadata=dict(example="knowark"))
    username = fields.Str(
        metadata=dict(example="amlopez"))
    email = fields.Str(
        metadata=dict(example="amlopez@example.com"))
    password = fields.Str(
        metadata=dict(example="secret"))
    refresh_token = fields.Str(
        data_key='refreshToken',
        metadata=dict(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c"))
    client = fields.Str(
        metadata=dict(example="data_server"))


class TokenSchema(Schema):
    refresh_token = fields.Str(
        data_key='refreshToken',
        metadata=dict(example="eyJhbG.eyJzdWIiOiIx.MjM5MadQssw5c"))
    access_token = fields.Str(
        data_key='accessToken',
        metadata=dict(example="eyJhbG.kpvaG4gRMyfQ.SflKxwssw5cdfs"))
