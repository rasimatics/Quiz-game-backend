
from marshmallow import Schema,fields,validate

class UserRegister(Schema):
    username = fields.Str(required=True,validate=[validate.Length(min=5,max=20)])
    email = fields.Email(required=True,validate=[validate.Length(min=3)])
    password = fields.Str(required=True,validate=[validate.Length(min=6,max=20)])
    isBot = fields.Bool(required=False)

class UserLogin(Schema):
    username = fields.Str(required=True,validate=[validate.Length(min=5,max=20)])
    password = fields.Str(required=True,validate=[validate.Length(min=6,max=20)])


    