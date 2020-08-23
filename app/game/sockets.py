from app import socketio
from flask_socketio import join_room, emit
from app.models import GameRoom, Player, Question, Word, User, PlayerAnswer
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

        gameroom.questions.append(question.id)

        word.usage += 1
        word.save()

        gameroom.word = word.word

        length = len(word.word)
        gameroom.members[0].found_letters = ["" for i in range(length-1)]
        gameroom.members[1].found_letters = ["" for i in range(length-1)]

        gameroom.currentQuestion = question.question
        gameroom.save()

    json_data = gameroom.to_json()
    socketio.emit('game-info', json.loads(json_data), data['room'])


@socketio.on('answer-question')
def check_answer(data):
    gameroom = GameRoom.objects(id=data['room']).first()
    player_answer = PlayerAnswer(
        username=data['username'], answer=data['answer'])
    gameroom.answers.append(player_answer)
    gameroom.save()

    member0 = gameroom.members[0]
    member1 = gameroom.members[1]

    if len(gameroom.answers) == 2:
        gameroom.bothAnswered = True
        gameroom.save()

    if gameroom.bothAnswered:
        user0 = gameroom.answers[0]
        user1 = gameroom.answers[1]

        question_object = gameroom.questions[-1]

        question = Question.objects(id=question_object.id).first()

        correctAnswer = int(question.answer[question.correct_index])

        # find index of found_letters
        i0 = get_index_of_word(gameroom.word,member0)
        i1 = get_index_of_word(gameroom.word,member1)
        
        if abs(int(user0.answer)-correctAnswer) > abs(int(user1.answer)-correctAnswer):
            if member0.name == user1.username:
                member0.found_letters[i0] = gameroom.word[i0-1]
            else:
                member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user1.username} found correct answer", "correct_answer": correctAnswer})
        elif abs(int(user0.answer)-correctAnswer) < abs(int(user1.answer)-correctAnswer):
            if member0.name == user0.username:
                member0.found_letters[i0] = gameroom.word[i0-1]
            else:
                member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user0.username} found correct answer", "correct_answer": correctAnswer})
        else:
            member0.found_letters[i0] = gameroom.word[i0-1]
            member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user0.username} and {user1.username} found correct answer", "correct_answer": correctAnswer})

        # Task get new question
        socketio.emit('game-info', data)


@socketio.on('guess-word')
def handle_guess(data):
    gameroom = GameRoom.objects(id=data['room']).first()
    if not gameroom.gameFinished:
        if gameroom.word.rstrip() == data['word']:
            data['info'] = f"{data['username']} found word and win the game!"

            if gameroom.members[0].name == data['username']:
                winner = gameroom.members[0].name
                loser = gameroom.members[1].name
            else:
                winner = gameroom.members[1].name
                loser = gameroom.members[0].name

            win_user = User.objects(username=winner).first()
            lose_user = User.objects(username=loser).first()

            finish_game(gameroom, win_user, lose_user)

            # Task modify point of user
            # Task clean the room and answer-question documents
        else:
            data['info'] = f"{data['username']} guessed wrong!"

        socketio.emit('game-info', data)
    else:
        socketio.emit('game-info', {"info": "Game finished"})
