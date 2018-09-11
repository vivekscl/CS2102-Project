from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config
from app.forms import ItemForm
from db import init_db
import os

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    """
    An app factory method that instantiates all the necessary dependencies and configurations. Any new libraries that
    need to be loaded into the app should be done here.
    :param config_name: Name of the configuration to load eg. production, development, etc.
    :return: the app with all libraries loaded into it
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    # Since the flask app runs twice when it's reloaded, we use this to run expensive operations only once.
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_db()
        app.logger.info("DB along with the required tables have been initialised")
    app.logger.info("All configurations have been set")
    return app
