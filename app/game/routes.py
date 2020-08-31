from flask_restful import Resource
from flask import make_response, jsonify
from flask_login import login_required,current_user
from app import api
from app.models import GameRoom, Player, Question,User
import time


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
            gameroom.save()

        # create a new room
        else:
            gameroom = GameRoom()
            gameroom.members.append(player)
            gameroom.save()
            g_id = gameroom.id

            time.sleep(10) # 5s change to 10s
            gameroom = GameRoom.objects(id=g_id).first()
            if gameroom.waiting:
                gameroom.hasBot = True
                gameroom.waiting = False
                bot = list(User.objects(isBot=True).aggregate([{'$sample':{"size":1}}]))[0]
                player = Player(name=bot['username'])
                gameroom.botName = bot['username']
                gameroom.members.append(player)
                gameroom.save()
            gameroom.save()
        return make_response(jsonify(gameroom),201)




api.add_resource(CreateOrJoin, '/start-game/')



