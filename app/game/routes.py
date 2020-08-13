from flask_restful import Resource
from flask import make_response, jsonify
from flask_login import login_required
from app import api
from app.models import GameRoom, Player


# join to existing room else create room
class CreateOrJoin(Resource):
    def post(self):
        gameroom = GameRoom.objects(
            waiting=True).order_by("created_at").first()
        player = Player(name="Rasim")
        # join existing room
        if gameroom:
            gameroom.waiting = False
            gameroom.members.append(player)
            gameroom.save()
            # start game
            # return success response

        # create a new room
        else:
            gameroom = GameRoom()
            gameroom.members.append(player)
            gameroom.save()
            # wait
            # if not user connect bot
            # start game
            # return success response

        return jsonify(gameroom)

api.add_resource(CreateOrJoin, '/start-game/')

