from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_restful import Api
from flask_cors import CORS




# create instance of extentsion
db = MongoEngine()
loginmanager = LoginManager()
api = Api()
cors = CORS()

loginmanager.login_message = 'Hello world'


from .users import routes

def create_app():
	app = Flask(__name__)

	app.config.from_object('config.Config')


	# initialize extensions
	db.init_app(app)
	loginmanager.init_app(app)
	api.init_app(app)
	cors.init_app(app, resources={"*": {"origins":"*"}})


	# register blueprints
	# app.register_blueprint(users)
	# app.register_blueprint(blueprint2)

	return app

