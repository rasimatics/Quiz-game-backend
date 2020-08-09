from flask_restful import Resource
from flask import make_response,jsonify
from flask_login import login_required
from app import api
from app.models import GameRoom,Player


class CreateOrJoin(Resource):
   pass

api.add_resource(CreateOrJoin,'/start-game/')

