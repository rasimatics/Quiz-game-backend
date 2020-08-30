from flask_restful import Resource
from flask import make_response, jsonify
from flask_login import login_required,current_user
from app import api
from app.models import GameRoom, Player, Question


# join to existing room else create room
class CreateOrJoin(Resource):
    @login_required
    def post(self): 
        gameroom = GameRoom.objects(waiting=True).order_by("created_at").first()
        player = Player(name=current_user.username)

        
        # join existing room
        if gameroom:
            gameroom.waiting = False
            gameroom.members.append(player)

        # create a new room
        else:
            gameroom = GameRoom()
            gameroom.members.append(player)
            # wait
            # if not user connect bot
            # start game
            # return success response

        gameroom.save()
        return make_response(jsonify(gameroom),201)




api.add_resource(CreateOrJoin, '/start-game/')



