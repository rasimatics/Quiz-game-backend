from flask import Blueprint, request, jsonify
from app.models import Users
from werkzeug.security import generate_password_hash
from flask_login import login_required, login_user, logout_user
from app import api
from flask_restful import Resource
from .utils import *



class Register(Resource):
    def post(self):
        data = request.json
        user = get_user(data['username'])
        if user:
            return {"Error": 'This username is taken'}, 404

        user = Users(username=data['username'], email=data['email'],
                    password=generate_password_hash(data['password']))
        user.save()
        return jsonify(user)

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

