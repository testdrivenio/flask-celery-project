from unittest import mock

import pytest

from project import db
from project.celery_utils import custom_celery_task
from project.users.models import User


# tasks

@custom_celery_task()
def successful_task(user_id):
    user = User.query.get(user_id)
    user.username = 'test'
    db.session.commit()


@custom_celery_task()
def throwing_no_retry_task():
    raise TypeError


@custom_celery_task()
def throwing_retry_task():
    raise Exception


# tests

def test_custom_celery_task(db, config, user):
    config.update(CELERY_TASK_ALWAYS_EAGER=True)

    successful_task.delay(user.id)

    assert User.query.get(user.id).username == 'test'


def test_throwing_no_retry_task(config):
    """
    If the exception is in EXCEPTION_BLOCK_LIST, should not retry the task
    """
    config.update(CELERY_TASK_ALWAYS_EAGER=True)
    config.update(CELERY_TASK_EAGER_PROPAGATES=True)

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(TypeError):
            throwing_no_retry_task.delay()

        mock_retry.assert_not_called()


def test_throwing_retry_task(config):
    config.update(CELERY_TASK_ALWAYS_EAGER=True)
    config.update(CELERY_TASK_EAGER_PROPAGATES=True)

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(Exception):
            throwing_retry_task.delay()

        mock_retry.assert_called()
        # assert 'countdown' in mock_retry.call_args.kwargs
        assert 'countdown' in mock_retry.call_args[1]
