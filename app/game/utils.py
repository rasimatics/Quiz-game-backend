import random

def getRandomIndex(modelName):
    count = modelName.objects.count()
    number = random.randint(0,1000)
    index = number % count  
    return index