import random

def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0,1000)
    index = number % count  
    return index



def finish_game(gameroom,winner,loser):
    gameroom.gameFinished = True
    gameroom.winner = winner.username
    gameroom.currentQuestion= ""
    gameroom.members[0].found_letters.clear()
    gameroom.members[1].found_letters.clear()
    gameroom.answers.clear()
    gameroom.questions.clear()
    gameroom.word = ""
    gameroom.save()

    winner.point+=100
    winner.win+=1
    winner.save()

    loser.lose+=1
    loser.save()