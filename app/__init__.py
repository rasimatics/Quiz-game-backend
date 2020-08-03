import os

from flask import Flask
from .blueprint1.routes import blueprint1
from .blueprint2.routes import blueprint2

# create instance of extentsion

def create_app():
	app = Flask(__name__)

	app.config.from_object('app.config')

	# initialize extensions

	# register blueprints
	app.register_blueprint(blueprint1)
	app.register_blueprint(blueprint2)

	return app

