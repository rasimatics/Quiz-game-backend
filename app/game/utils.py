import random
from app.models import GameRoom, PlayerAnswer

# get random index related to model objects
def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0, 1000)
    index = number % count
    return index


# game finish: modify gameroom
def finish_game(gameroom, winner, loser):
    gameroom.gameFinished = True
    gameroom.winner = winner.username
    gameroom.currentQuestion = ""
    gameroom.update(set__questions=[])
    gameroom.update(set__answers=[])
    gameroom.update(set__members__0__found_letters=[])
    gameroom.update(set__members__1__found_letters=[])
    gameroom.word = ""
    gameroom.save()

    winner.point += 100
    winner.win += 1
    winner.save()

    loser.lose += 1
    loser.save()


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
