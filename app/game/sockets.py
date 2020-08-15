from app import socketio
from flask_socketio import join_room,emit
from app.models import GameRoom, Player, Question
from flask import jsonify
import json

@socketio.on('join-room')
def handle_join_room(data):
    join_room(data['room'])
    socketio.emit('join-room-info', {"info":"connected"}, data['room'])
"""
{
 "room":"123",
 "username":"rasimatics"
} 
"""


# disconnect
# @socketio.on('disconnect')
# def handle_disconnect():


# start game -> game information
@socketio.on('start-game')
def handle_start(data):
    gameroom = GameRoom.objects(id=data['room']).first()
    json_data = gameroom.to_json()
    socketio.emit('game-info',json.loads(json_data))



# give information about game-status
# def game_info() different for each user related to username

# answer question
# def check_answer()

# guess word
# def check_guess()
