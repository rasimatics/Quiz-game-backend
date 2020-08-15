from app import socketio
from flask_socketio import join_room,emit

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


# join to the room
# def join_room()

# give information about game-status
# def game_info() different for each user related to username

# answer question
# def check_answer()

# guess word
# def check_guess()
