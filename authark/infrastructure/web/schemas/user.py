from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(required=True, example="amlopez")
    email = fields.Email(required=True, example="amlopez@nubark.com")
    password = fields.Str(required=True, load_only=True, example="secret")
