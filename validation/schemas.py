from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    username = fields.String(
        required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class TextGenerationSchema(Schema):
    prompt = fields.String(
        required=True, validate=validate.Length(min=3, max=500))
