from flask.ext.cache import Cache
from flask.ext.login import LoginManager

from pasteur.models import User

# Setup flask cache
cache = Cache()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
