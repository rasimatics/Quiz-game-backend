from flask import Blueprint

blueprint1 = Blueprint('blueprint',__name__)

@blueprint1.route('/')
def index():
	return 'Blueprint1'