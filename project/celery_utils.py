from celery import current_app as current_celery_app
from celery import Task


def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")

    # Set Flask application object on the Celery application.
    if not hasattr(celery, 'flask_app'):
        celery.flask_app = app

    celery.Task = AppContextTask

    return celery


class AppContextTask(Task):
    """
    Celery task running within a Flask application context.
    """

    def __call__(self, *args, **kwargs):
        # self.app is the Celery app instance
        with self.app.flask_app.app_context():
            Task.__call__(self, *args, **kwargs)
