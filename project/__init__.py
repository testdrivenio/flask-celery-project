import os

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

from project.celery_utils import make_celery
from project.config import config


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
csrf = CSRFProtect()
socketio = SocketIO()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ext_celery.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])

    # register blueprints
    from project.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
