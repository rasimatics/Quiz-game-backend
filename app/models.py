from app import db,bcrypt
import datetime
import random


class User(db.Document):
    username = db.StringField()
    password = db.BinaryField()
    email = db.EmailField()
    point = db.IntField(default=500)
    win = db.IntField(default=0)
    lose = db.IntField(default=0)
    isBot = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        

    def check_password(self,password):
        return bcrypt.check_password_hash(pw_hash=self.password,password=password)
        

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

class Player(db.EmbeddedDocument):
    sid = db.StringField(default="")
    name = db.StringField()
    guess_chances = db.IntField(default=2)
    found_letters = db.ListField(db.StringField(),default=list)


class Word(db.Document):
    word = db.StringField(max_length=7)
    usage = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Question(db.Document):
    question = db.StringField()
    answer = db.ListField(db.StringField())
    correct_index = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


class PlayerAnswer(db.EmbeddedDocument):
    username = db.StringField()
    answer = db.StringField()


class GameRoom(db.Document):
    word = db.StringField(default="")
    waiting = db.BooleanField(default=True)
    currentQuestion = db.StringField(default="")
    gameFinished = db.BooleanField(default=False)
    winner = db.ListField(db.StringField())
    bothAnswered = db.BooleanField(default=False)
    members = db.ListField(db.EmbeddedDocumentField(Player),default=list)
    answers = db.ListField(db.EmbeddedDocumentField(PlayerAnswer))
    questions = db.ListField(db.StringField())
    hasBot = db.BooleanField(default=False)
    botName = db.StringField(default="")
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)





