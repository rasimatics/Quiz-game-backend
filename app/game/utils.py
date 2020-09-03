import random
from app.models import GameRoom, PlayerAnswer
from mongoengine import Q

# get random index related to model objects
def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0, 1000)
    index = number % count
    return index


# game finish: modify gameroom
def finish_game(gameroom, winner, loser,draw=False):
    gameroom.gameFinished = True
    gameroom.currentQuestion = ""
    gameroom.update(set__questions=[])
    gameroom.update(set__answers=[])
    gameroom.update(set__members__0__found_letters=[])
    gameroom.update(set__members__1__found_letters=[])
    gameroom.word = ""

    # both users found all letters
    if draw:
        gameroom.winner.append(winner.username)
        gameroom.winner.append(loser.username)
        winner.point += 50
        loser.point += 50
        winner.win += 1
        loser.win += 1

    # one user found all letters
    else:
        gameroom.winner.append(winner.username)
        winner.point += 100
        winner.win += 1
        loser.lose += 1

    gameroom.save()
    loser.save()
    winner.save()


# get index of found_letter
def get_index_of_word(word, member):
    i = -1
    for a in range(len(word)):
        if member.found_letters[i] == "":
            break
        i -= 1
    return i


# get room related to id
def get_gameroom(room):
    gameroom = GameRoom.objects(id=room).first()
    return gameroom


# make found_letters empty string size of word
def empty_list_word(gameroom, length):
    gameroom.members[0].found_letters = ["" for i in range(length-1)]
    gameroom.members[1].found_letters = ["" for i in range(length-1)]


# get answer related to the correct answer
def get_answer(gameroom, correctAnswer):
    answers = []
    length = len(correctAnswer)
    correctAnswer = int(correctAnswer)
    increment = random.randint(0, 10**(length-1))
    high = random.randint(correctAnswer, correctAnswer*10)
    low = random.randint(0, correctAnswer)
    answers.extend((correctAnswer, correctAnswer+increment, correctAnswer-increment, high, low))
    index = random.randint(0, 3)
    player_answer = PlayerAnswer(username=gameroom.botName, answer=str(answers[index]))
    gameroom.answers = [player_answer,]
    gameroom.save()

# get gameroom with session id of socket
def find_room_with_sid(sid):
    gameroom = GameRoom.objects.filter(Q(members__0__sid=sid) or Q(members__1__sid=sid)).first()
    return gameroom


# get loser,winner from gameroom with sid of socket
def find_member_with_sid(gameroom,sid):
    member0 = gameroom.members[0]
    member1 = gameroom.members[1]

    if member0.sid == sid:
        return member0.name,member1.name
    return member1.name,member0.name

