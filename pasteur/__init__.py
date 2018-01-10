#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Brady Hurlburt'
__email__ = 'bradyhurlburt@gmail.com'
__version__ = '0.1'

from flask import Flask

from pasteur.controllers.main import main
from pasteur.models import db

from pasteur.extensions import (
    cache,
    login_manager
)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. pasteur.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)

    # initialize the cache
    cache.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # register our blueprints
    app.register_blueprint(main)

    return app
