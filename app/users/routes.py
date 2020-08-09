from flask import Blueprint, request, jsonify
from app.models import User
from werkzeug.security import generate_password_hash
from flask_login import login_required, login_user, logout_user
from app import api
from flask_restful import Resource
from .utils import *
from .schema import *




class Register(Resource):
    def post(self):
        schema = Userschema()
        data = request.get_json(force=True)
        errors = schema.validate(data)
        if errors:
            return errors, 422
        data = schema.dump(data)
        user = User(username=data['username'],password=data['password'],email=data['email'])
        user.save()
        return data

api.add_resource(Register, '/user/register/')



class Login(Resource):
    def post(self):
        data = request.json
        username = data['username']
        password = data['password']
        user = get_user(username)

        if user and user.check_password(password):
            login_user(user)
            return {"Info": "User signed in!"}
        else:
            return {"Error": "User cridentials are not correct"}, 404

api.add_resource(Login, '/user/login/')


class Logout(Resource):
    def get(self):
        logout_user()
        return {"Info": "User loged out!"}

api.add_resource(Logout, '/user/logout/')

