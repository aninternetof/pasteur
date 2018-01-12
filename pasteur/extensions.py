import eventlet
eventlet.monkey_patch()
from flask.ext.cache import Cache
from flask.ext.login import LoginManager
from flask_socketio import SocketIO

from pasteur.models import User

from pasteur.tasks.thermostat import Thermostat

# Setup flask cache
cache = Cache()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"

socketio = SocketIO()

thermostat = Thermostat(socketio)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
