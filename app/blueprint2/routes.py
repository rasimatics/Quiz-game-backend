from flask import Blueprint

blueprint2 = Blueprint('blueprint2',__name__)

@blueprint2.route('/index')
def index():
	return 'Blueprint2'