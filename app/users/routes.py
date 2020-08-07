from flask import Blueprint, request, jsonify
from app.models import Users
from werkzeug.security import generate_password_hash
from flask_login import  login_manager,login_required,login_user,logout_user
from app import loginmanager

users = Blueprint('users', __name__, url_prefix='/user')


def get_user(username):
    user = Users.objects(username=username).first()
    return user if user is not None else None

@loginmanager.user_loader
def load_user(username):
    return get_user(username)


@users.route('/register/', methods=['POST'])
def register():
    data = request.json
    user = Users.objects.filter(username=data['username'])
    if user:
        return {"Error":'This username is taken'},404
    user = Users(username=data['username'], email=data['email'], password=generate_password_hash(data['password']))
    user.save()
    return jsonify(user)


@users.route('/login/',methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = get_user(username)

    if user and user.check_password(password):
        login_user(user)
        return {"Info":"User signed in!"}
    else:
        return {"Error":"User cridentials are not correct"},404


@users.route('/logout/',methods=['GET'])
def logout():
    logout_user()
    return {"Info":"User loged out!"}



@users.route('/index/',methods=['GET'])
@login_required
def index():
    return {"Info":"HAHAHA"}
