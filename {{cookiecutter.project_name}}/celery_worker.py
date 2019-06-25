"""The celery worker has to be started to handle the tasks of celery.

This pattern is followed because we're instantiating the flask application through
flask's application factory. The context of the application is required.
"""
from {{cookiecutter.application_name}}import create_app
from {{cookiecutter.application_name}}import celery
import logging

logger = logging.getLogger('celery')
logger.setLevel(logging.DEBUG)
logger.propagate = True
app = create_app()
app.app_context().push()

