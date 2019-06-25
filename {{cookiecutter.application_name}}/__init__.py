"""
Initializing the application over here.
"""

import logging
import coloredlogs

from flask import Flask
from celery import Celery
from dynaconf import FlaskDynaconf, settings
from logging.config import dictConfig


celery = Celery(__name__)
flask_dynaconf = FlaskDynaconf()

logger = logging.getLogger(__name__)


def init_celery(app, celery):
    """
    Initializes the celery instance for the given application.

    This is requried because we're following the application factory pattern.

    Parameters
    ----------
    app -- The flask application instance
    celery -- The celery instance.

    Returns
    -------
    None
    """
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    logger.debug("Instantiated celery for the application: {}".format(app.name))
    return None


def create_app(config_file=None):
    """
    App factory.

    Create an application instance and return it.

    :param config_file: TODO: Future usecase for a config file based app instantiation.
    :return:
    """

    app = Flask(__name__)

    # Initialize the DynaConf for the application
    flask_dynaconf.init_app(app)

    # Initialize celery for the application
    init_celery(app, celery)


    # Update celery configuration
    celery.conf.update(
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
    )

    # Initialize logs with custom config.
    dictConfig(settings.LOGGING_CONFIG)

    # Initialize colored logs.
    coloredlogs.install(level=logging.DEBUG)

    # Register routes here
    # Importing here to avoid circular import on celery.
    
    # Api blueprint

    app.register_blueprint(api, url_prefix="/api/")

    logger.info("Initialized (colored) logs")

    return app

