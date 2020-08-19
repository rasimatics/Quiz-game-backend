from app import socketio
from flask_socketio import join_room,emit
from app.models import GameRoom, Player, Question, Word, AnsweredQuestion, PlayerAnswer
from flask import jsonify
import json
from .utils import *

@socketio.on('join-room')
def handle_join_room(data):
    join_room(data['room'])
    data['info'] = 'connected'
    socketio.emit('join-room-info', data, data['room'])
    
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
# only first time when game starts
@socketio.on('start-game')
def handle_start(data):
    gameroom = GameRoom.objects(id=data['room']).first()

    word = Word.objects[getRandomIndex(Word)]
    question = Question.objects[getRandomIndex(Question)]

    answered_question = AnsweredQuestion(question=question.id,room=gameroom.id)
    answered_question.save()

    word.usage += 1
    word.save()

    gameroom.members[0].word = word.word
    gameroom.members[1].word = word.word

    length = len(word.word)
    gameroom.members[0].found_letters = ["" for i in range(length-1)]
    gameroom.members[1].found_letters = ["" for i in range(length-1)]
   
    gameroom.currentQuestion = question.question
    gameroom.save()
    
    json_data = gameroom.to_json()
    socketio.emit('game-info',json.loads(json_data),data['room'])


@socketio.on('answer-question')
def check_answer(data):
    answer_question = AnsweredQuestion.objects(room=data['room']).first()
    player_answer = PlayerAnswer(username=data['username'],answer=data['answer'])
    answer_question.answers.append(player_answer)
    answer_question.save()

    # check both answered or not
    


# guess word
# def check_guess()
