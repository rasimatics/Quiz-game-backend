from flask_restful import Resource
from flask import make_response,jsonify
from flask_login import login_required
from app import api
from app.models import GameRoom,Player

# join to existing room else create room
class CreateOrJoin(Resource):
   pass
"""
   if waiting room exists:
      join to this room
      game info (start game)
   else:
      create a new room
      after 10s get request from front (no waiting room)
      join bot player
      game info (start game)(return game data(questions and word))
"""

api.add_resource(CreateOrJoin,'/start-game/')



