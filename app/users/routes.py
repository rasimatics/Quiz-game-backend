from flask import  request, jsonify,make_response
from flask_login import  login_user, logout_user
from app import api
from flask_restful import Resource
from .utils import *
from .schema import *


class Register(Resource):
    def post(self):
        
        # json validation
        schema = UserRegister()
        data = request.get_json(force=True)
        errors = schema.validate(data)
        if errors:
            return errors, 422
        data = schema.dump(data)

        # check uniqueness
        check_username = User.objects(username=data['username']).first()
        check_email= User.objects(email=data['email']).first()

        if check_username and check_email:
            return make_response(jsonify({"Error":"Username and email were taken"}),400)
        if check_username:
            return make_response(jsonify({"Username":"This username is taken"}),400)
        if check_email:
            return make_response(jsonify({"Email":"This email is taken"}),400)

        # save user in db
        user = User(username=data['username'],password=data['password'],email=data['email'])
        user.save()

        return make_response(jsonify(user),201)

api.add_resource(Register, '/user/register/')



class Login(Resource):
    def post(self):
        schema = UserLogin()
        data = request.get_json(force=True)
        errors = schema.validate(data)
        if errors:
            return errors, 422
        data = schema.dump(data)
        username = data['username']
        password = data['password']

        user = get_user(username)

        if user and user.check_password(password):
            login_user(user)
            return make_response(jsonify({"Info": "User signed in!"}),200)
        else:
            return make_response(jsonify({"Error": "User cridentials are not correct"}), 400)

api.add_resource(Login, '/user/login/')


class Logout(Resource):
    def get(self):
        logout_user()
        return make_response(jsonify({"Info": "User loged out!"}),200)

api.add_resource(Logout, '/user/logout/')

