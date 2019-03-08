from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(example="amlopez")
    email = fields.Email(example="amlopez@nubark.com")
    password = fields.Str(example="secret")
