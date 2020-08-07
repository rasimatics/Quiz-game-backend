from flask import Blueprint
from app.models import Users

blueprint1 = Blueprint('blueprint',__name__)

@blueprint1.route('/')
def index():
	user = Users(name="Rasim3",email="rasim@gmail.com")
	user.save()
	return 'Blueprint1'