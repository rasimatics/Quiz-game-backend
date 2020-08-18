from app import create_app
from app import socketio

if __name__ == '__main__':
    app = create_app()
    socketio.run(app)
    