from flask import Flask

from flask_mongoengine import MongoEngine




# create instance of extentsion
db = MongoEngine()


from .users.routes import blueprint1
from .blueprint2.routes import blueprint2

def create_app():
	app = Flask(__name__)

	app.config.from_object('app.config.Config')


	# initialize extensions
	db.init_app(app)



	# register blueprints
	app.register_blueprint(blueprint1)
	app.register_blueprint(blueprint2)

	return app

