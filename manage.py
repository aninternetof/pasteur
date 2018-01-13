#!/usr/bin/env python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from pasteur import create_app
from pasteur.models import db, User
from pasteur.extensions import socketio, thermostat

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('PASTEUR_ENV', 'dev')
app = create_app('pasteur.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """

    db.create_all()

@manager.command
def add_user(username, password):
    """ Create user
    """
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    print("Added user {}".format(username))

@manager.command
def run():
    """ Run with socketio
    """
    socketio.start_background_task(thermostat.run_thermostat)
    socketio.run(app, port=5000, host='0.0.0.0', use_reloader=False)

if __name__ == "__main__":
    manager.run()
