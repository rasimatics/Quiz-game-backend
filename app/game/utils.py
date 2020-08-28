import random
from app.models import GameRoom

# get random index related to model objects
def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0,1000)
    index = number % count  
    return index


# game finish: modify gameroom
def finish_game(gameroom,winner,loser):
    gameroom.gameFinished = True
    gameroom.winner = winner.username
    gameroom.currentQuestion= ""
    gameroom.update(set__questions=[])
    gameroom.update(set__answers=[])
    gameroom.update(set__members__0__found_letters=[])
    gameroom.update(set__members__1__found_letters=[])
    gameroom.word = ""
    gameroom.save()

    winner.point+=100
    winner.win+=1
    winner.save()

    loser.lose+=1
    loser.save()


# get index of found_letter
def get_index_of_word(word,member):
    i = -1
    for a in range(len(word)):
        if member.found_letters[i] == "":
            break
        i -= 1
    return i


def get_gameroom(room):
    gameroom = GameRoom.objects(id=room).first()
    return gameroom