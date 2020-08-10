from flask_restful import Resource
from flask import make_response, jsonify
from flask_login import login_required
from app import api
from app.models import GameRoom, Player


# join to existing room else create room
class CreateOrJoin(Resource):

    def post(self):
        gameroom = GameRoom.objects(waiting=True).order_by("created_at").first()
        player = Player(name="Rasim")
        # join existing room
        if gameroom:
           gameroom.waiting = False
           gameroom.members.append(player)
           gameroom.save()
           # start game

        # create a new room
        else:
           gameroom = GameRoom()
           gameroom.members.append(player)
           gameroom.save()
           # wait
           # if not user connect bot
           # start game

        return jsonify(gameroom)


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

api.add_resource(CreateOrJoin, '/start-game/')
