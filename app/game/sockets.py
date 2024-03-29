from app import socketio
from app.models import GameRoom, Player, Question, Word, User, PlayerAnswer
from flask_socketio import join_room, emit
from flask import jsonify,request
from .utils import *
import random
import json


# after room created join room
@socketio.on('join-room')
def handle_join_room(data):
    user = User.objects(username=data['username']).first()
    # update point of user
    point = user.point - 50
    user.update(set__point=point)

    # save sid of player
    gameroom = get_gameroom(data['room'])
    member0 = gameroom.members[0]
    member1 = gameroom.members[1]
    if member0.name == data['username']:
        member0.sid = request.sid
    else:
        member1.sid = request.sid
    gameroom.save()

    join_room(data['room'])

    data['info'] = 'connected'
    socketio.emit('join-room-info', data, data['room'])


# add question to db
@socketio.on('add-question')
def handle_add(data):
    question = Question(question=data['question'],answer=[data['answer'],])
    question.save()
    socketio.emit('game-info', data)


# disconnect
@socketio.on('disconnect')
def handle_disconnect():
    gameroom = find_room_with_sid(request.sid)
    loserName,winnerName = find_member_with_sid(gameroom,request.sid)
    loser = User.objects(username=loserName).first()
    winner = User.objects(username=winnerName).first()
    finish_game(gameroom,winner,loser)

    json_data = gameroom.to_json()
    socketio.emit('game-info', json.loads(json_data), str(gameroom.id))


# only first time when game starts
@socketio.on('start-game')
def handle_start(data):
    gameroom = get_gameroom(data['room'])

    if gameroom.word == "":

        # get word and question
        word = Word.objects[getRandomIndex(Word)]
        question = Question.objects[getRandomIndex(Question)]
        gameroom.questions.append(str(question.id))

        # assign word to gameroom
        word.usage += 1
        word.save()
        gameroom.word = word.word
        length = len(word.word)
        empty_list_word(gameroom,length)

        # assign question to  gameroom
        gameroom.currentQuestion = question.question


        # in case bot exist get bot's answer
        if gameroom.hasBot:
            correctAnswer = question.answer[question.correct_index]
            get_answer(gameroom,correctAnswer)

        # save all changes
        gameroom.save()


    json_data = gameroom.to_json()
    socketio.emit('game-info', json.loads(json_data), data['room'])


# user answer question
@socketio.on('answer-question')
def check_answer(data):
    gameroom = get_gameroom(data['room'])
    player_answer = PlayerAnswer(
        username=data['username'], answer=data['answer'])
    gameroom.answers.append(player_answer)
    gameroom.save()

    member0 = gameroom.members[0]
    member1 = gameroom.members[1]

    # both users answered to the question
    if len(gameroom.answers) == 2:
        gameroom.bothAnswered = True
        gameroom.save()

    # check answers
    if gameroom.bothAnswered:
        # get users' answers
        user0 = gameroom.answers[0]
        user1 = gameroom.answers[1]

        question_id = gameroom.questions[-1]
        question = Question.objects(id=question_id).first()
        correctAnswer = int(question.answer[question.correct_index])

        # find index of found_letters
        i0 = get_index_of_word(gameroom.word,member0)
        i1 = get_index_of_word(gameroom.word,member1)
        
        # user1 found correct answer
        if abs(int(user0.answer)-correctAnswer) > abs(int(user1.answer)-correctAnswer):
            if member0.name == user1.username:
                member0.found_letters[i0] = gameroom.word[i0-1]
            else:
                member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user1.username} found correct answer", "correct_answer": correctAnswer}, data['room'])
        
        # user0 found correct answer
        elif abs(int(user0.answer)-correctAnswer) < abs(int(user1.answer)-correctAnswer):
            if member0.name == user0.username:
                member0.found_letters[i0] = gameroom.word[i0-1]
            else:
                member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user0.username} found correct answer", "correct_answer": correctAnswer}, data['room'])
        
        # both user found correct answer
        else:
            member0.found_letters[i0] = gameroom.word[i0-1]
            member1.found_letters[i1] = gameroom.word[i1-1]
            gameroom.save()

            socketio.emit(
                'answer-info', {"info": f"{user0.username} and {user1.username} found correct answer", "correct_answer": correctAnswer}, data['room'])

        # check user found all letters or not
        firstuser = User.objects(username=member0.name).first()
        seconduser = User.objects(username=member1.name).first()

        # if both user found all letters
        if member0.found_letters[0] != "" and member1.found_letters[0] != "" :
            finish_game(gameroom,firstuser,seconduser,True)
            socketio.emit('answer-info', {"info": "Game finished"}, data['room'])

        # member0 found all letters
        elif member0.found_letters[0] != "":
            finish_game(gameroom,firstuser,seconduser)
            socketio.emit('answer-info', {"info": "Game finished"}, data['room'])

        # member1 found all letters
        elif member1.found_letters[0] != "":
            finish_game(gameroom,seconduser,firstuser)
            socketio.emit('answer-info', {"info": "Game finished"}, data['room'])
        
        # none of users found all letters game continues
        else:
            question = Question.objects[getRandomIndex(Question)]
            while str(question.id) in gameroom.questions:
                question = Question.objects[getRandomIndex(Question)]
    
            gameroom.questions.append(str(question.id))
            gameroom.currentQuestion = question.question
            gameroom.bothAnswered = False
            gameroom.update(set__answers=[])
            gameroom.save()
             
            #  in case bot exist get bot's answer
            if gameroom.hasBot:
                correctAnswer = question.answer[question.correct_index]
                get_answer(gameroom,correctAnswer)



        json_data = gameroom.to_json()
        socketio.emit('game-info', json.loads(json_data), data['room'])


# user attempt to guess word
@socketio.on('guess-word')
def handle_guess(data):
    gameroom = get_gameroom(data['room'])
    if not gameroom.gameFinished:

        if gameroom.members[0].name == data['username']:
            guessed_user = gameroom.members[0]
            other_user = gameroom.members[1]
        else:
            guessed_user = gameroom.members[1]
            other_user = gameroom.members[0]

        # decrease number of guesses
        guessed_user.guess_chances-=1
        gameroom.save()

        if gameroom.word.rstrip() == data['word']:
            data['info'] = f"{data['username']} found word and win the game!"


            win_user = User.objects(username=guessed_user.name).first()
            lose_user = User.objects(username=other_user.name).first()

            finish_game(gameroom, win_user, lose_user)
        else:
            data['info'] = f"{data['username']} guessed wrong!"
            socketio.emit('guess-info', data, data['room'])

    else:
        socketio.emit('guess-info', {"info": "Game finished"}, data['room'])

    json_data = gameroom.to_json()
    socketio.emit('game-info', json.loads(json_data), data['room'])
