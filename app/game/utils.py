import random

def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0,1000)
    index = number % count  
    return index



def finish_game(gameroom,winner,loser):
    gameroom.gameFinished = True
    gameroom.winner = winner.username
    gameroom.save()

    winner.win+=1
    winner.save()

    loser.lose+=1
    loser.save()