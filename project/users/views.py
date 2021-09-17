import random
import logging
from string import ascii_lowercase

import requests
from celery.result import AsyncResult
from flask import Blueprint, render_template, flash, abort, request, Response, jsonify, current_app

from . import users_blueprint
from project import csrf, db
from project.users.forms import YourForm
from project.users.models import User
from project.users.tasks import (
    sample_task,
    task_add_subscribe,
    task_process_notification,
    task_send_welcome_email,
)


def random_username():
    username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
    return username


def api_call(email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception('random processing error')

    # used for simulating a call to a third-party api
    requests.post('https://httpbin.org/delay/5')


@users_blueprint.route('/form/', methods=('GET', 'POST'))
def subscribe():
    form = YourForm()
    if form.validate_on_submit():
        task = sample_task.delay(form.email.data)
        return jsonify({
            'task_id': task.task_id,
        })
    return render_template('form.html', form=form)


@users_blueprint.route('/task_status/', methods=('GET', 'POST'))
def task_status():
    task_id = request.args.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        if task.state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': task.state,
                'error': error,
            }
        else:
            response = {
                'state': task.state,
            }
        return jsonify(response)


@users_blueprint.route('/webhook_test/', methods=('POST', ))
@csrf.exempt
def webhook_test():
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post('https://httpbin.org/delay/5')
    return 'pong'


@users_blueprint.route('/webhook_test2/', methods=('POST', ))
@csrf.exempt
def webhook_test_2():
   task = task_process_notification.delay()
   current_app.logger.info(task.id)
   return 'pong'


@users_blueprint.route('/form_ws/', methods=('GET', 'POST'))
def subscribe_ws():
    form = YourForm()
    if form.validate_on_submit():
        task = sample_task.delay(form.email.data)
        return jsonify({
            'task_id': task.task_id,
        })
    return render_template('form_ws.html', form=form)


@users_blueprint.route('/transaction_celery/', methods=('GET', 'POST'))
def transaction_celery():
    try:
        username = random_username()
        user = User(
            username=f'{username}',
            email=f'{username}@test.com',
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise

    current_app.logger.info(f'user {user.id} {user.username} is persistent now')
    task_send_welcome_email.delay(user.id)
    return 'done'


@users_blueprint.route('/user_subscribe/', methods=('GET', 'POST'))
def user_subscribe():
    form = YourForm()
    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(
                username=form.username.data
            ).first()
            if user:
                user_id = user.id
            else:
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                )
                db.session.add(user)
                db.session.commit()
                user_id = user.id
        except Exception as e:
            db.session.rollback()
            raise

        task_add_subscribe.delay(user_id)
        return 'sent task to Celery successfully'

    return render_template('user_subscribe.html', form=form)
