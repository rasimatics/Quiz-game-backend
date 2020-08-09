from app.models import User
from app import loginmanager


def get_user(username):
    user = User.objects(username=username).first()
    return user if user is not None else None


@loginmanager.user_loader
def load_user(username):
    return get_user(username)