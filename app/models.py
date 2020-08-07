from app import db

class Users(db.Document):
    name = db.StringField()
    email = db.StringField()
