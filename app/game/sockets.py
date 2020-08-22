from app import socketio
from flask_socketio import join_room,emit
from app.models import GameRoom, Player, Question, Word, User, AnsweredQuestion, PlayerAnswer
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

    if gameroom.word == "":
        word = Word.objects[getRandomIndex(Word)]
        question = Question.objects[getRandomIndex(Question)]

        answered_question = AnsweredQuestion(questions=[question.id,],room=gameroom.id)
        answered_question.save()

        word.usage += 1
        word.save()

        gameroom.word = word.word

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


    if len(answer_question.answers) == 2:
        answer_question.bothAnswered = True
        answer_question.save()
    
    if answer_question.bothAnswered:
        user0 = answer_question.answers[0]
        user1 = answer_question.answers[1]

        question_object = answer_question.questions[-1]


        question = Question.objects(id=question_object.id).first()

        correctAnswer = int(question.answer[question.correct_index])

        # Task1 actions in each case
        if abs(int(user0.answer)-correctAnswer) > abs(int(user1.answer)-correctAnswer):
            socketio.emit('answer-info',{"info":f"{user1.username} found correct answer","correct_answer":correctAnswer })
        elif abs(int(user0.answer)-correctAnswer) < abs(int(user1.answer)-correctAnswer):
            socketio.emit('answer-info',{"info":f"{user0.username} found correct answer","correct_answer":correctAnswer })
        else:
            socketio.emit('answer-info',{"info":f"{user0.username} and {user1.username} found correct answer","correct_answer":correctAnswer })

        # socket emit all needed data
        socketio.emit('game-info',{"info":"round finished"})

    


@socketio.on('guess-word')
def handle_guess(data):
    gameroom = GameRoom.objects(id=data['room']).first()
    if gameroom.word.rstrip() == data['word']:
        data['info'] = f"{data['username']} found word and win the game!"

        if gameroom.members[0].name == data['username']:
            winner = gameroom.members[0].name
            loser = gameroom.members[1].name
        else:
            winner = gameroom.members[1].name
            loser = gameroom.members[0].name

        gameroom.gameFinished = True
        gameroom.winner = winner
        gameroom.save()

        user = User.objects(username=winner).first()
        user.win+=1
        user.save()

        user = User.objects(username=loser).first()
        user.lose+=1
        user.save()

        # Task modify point of user
        # Task clean the room and answer-question documents
    else:
        data['info'] = f"{data['username']} guessed wrong!"

    socketio.emit('game-info',data)
