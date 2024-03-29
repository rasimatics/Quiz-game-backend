from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt



# create instance of extentsion
db = MongoEngine()
loginmanager = LoginManager()
api = Api()
cors = CORS()
socketio = SocketIO(logger=True,engineio_logger=True,cors_allowed_origins="*",ping_timeout=5)
bcrypt = Bcrypt()


from .users import routes
from .game import  routes, sockets

def create_app():
	app = Flask(__name__)
	app.config.from_object('config.Config')


	# initialize extensions
	db.init_app(app)
	loginmanager.init_app(app)
	api.init_app(app)
	cors.init_app(app, resources={"*": {"origins":"*"}})
	socketio.init_app(app)
	bcrypt.init_app(app)


	return app

