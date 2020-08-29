from app import db
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import random, string



class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.EmailField()
    point = db.IntField(default=500)
    win = db.IntField(default=0)
    lose = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def clean(self):
        super(User,self).clean()
        self.password = generate_password_hash(self.password)
        

    def check_password(self,password):
        return check_password_hash(self.password,password)

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
    name = db.StringField()
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
    winner = db.StringField(default="")
    bothAnswered = db.BooleanField(default=False)
    members = db.ListField(db.EmbeddedDocumentField(Player),default=list)
    answers = db.ListField(db.EmbeddedDocumentField(PlayerAnswer))
    questions = db.ListField(db.StringField())
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)





