
from marshmallow import Schema,fields,validate

class Userschema(Schema):
    username = fields.Str(required=True,validate=[validate.Length(min=5,max=20)])
    email = fields.Email(required=True,validate=[validate.Length(min=3,error="Email is not valid")])
    password = fields.Str(required=True,validate=[validate.Length(min=6,max=20)])
