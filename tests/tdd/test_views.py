import os
from unittest import mock

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage

from project.tdd import tasks
from project.tdd.models import Member


def test_get(client, db):
    response = client.get(url_for('tdd.member_signup'))
    assert response.status_code == 200


def test_post(client, db, member_factory, monkeypatch):
    fake_member = member_factory.build()
    avatar_full_path = os.path.join(
        current_app.config['UPLOADS_DEFAULT_DEST'],
        fake_member.avatar
    )

    data = {
        'username': fake_member.username,
        'email': fake_member.email,
        'avatar': FileStorage(
            stream=open(avatar_full_path, "rb"),
            filename="test.jpg",
            content_type="image/jpeg",
        )
    }

    mock_generate_avatar_thumbnail_delay = mock.MagicMock(name="generate_avatar_thumbnail")
    monkeypatch.setattr(tasks.generate_avatar_thumbnail, 'delay', mock_generate_avatar_thumbnail_delay)

    response = client.post(
        url_for('tdd.member_signup'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200

    member = Member.query.filter_by(username=fake_member.username).first()
    assert member
    assert member.avatar
    mock_generate_avatar_thumbnail_delay.assert_called_with(
        member.id
    )


def test_post_fail(client, db, member_factory):
    fake_member = member_factory.build()

    form_data = {
        'username': fake_member.username,
    }

    response = client.post(url_for('tdd.member_signup'), data=form_data)
    assert response.status_code == 200

    member = Member.query.filter_by(username=fake_member.username).first()
    assert not member
