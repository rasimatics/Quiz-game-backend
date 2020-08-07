from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager



# create instance of extentsion
db = MongoEngine()
loginmanager = LoginManager()
loginmanager.login_message = 'Hello world'

from .users.routes import users
from .blueprint2.routes import blueprint2

def create_app():
	app = Flask(__name__)

	app.config.from_object('config.Config')


	# initialize extensions
	db.init_app(app)
	loginmanager.init_app(app)


	# register blueprints
	app.register_blueprint(users)
	app.register_blueprint(blueprint2)

	return app

