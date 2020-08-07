from app import db
from werkzeug.security import check_password_hash
import datetime

class Users(db.Document):
    username = db.StringField(required=True,unique=True)
    password = db.StringField(required=True)
    email = db.EmailField(required=True,unique=True)
    point = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


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

