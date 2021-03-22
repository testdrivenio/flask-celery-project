import os

from celery import shared_task
from flask import current_app
from PIL import Image

from project import db
from project.tdd.models import Member


@shared_task(name='generate_avatar_thumbnail')
def generate_avatar_thumbnail(member_pk):
    member = Member.query.get(member_pk)

    full_path = os.path.join(
        current_app.config['UPLOADS_DEFAULT_DEST'],
        member.avatar
    )

    thumbnail_path = f'{member.id}-avatar-thumbnail.jpg'
    thumbnail_full_path = os.path.join(
        current_app.config['UPLOADS_DEFAULT_DEST'],
        thumbnail_path
    )

    im = Image.open(full_path)
    size = (100, 100)
    im.thumbnail(size)
    im.save(thumbnail_full_path, 'JPEG')

    member.avatar_thumbnail = thumbnail_path
    db.session.add(member)
    db.session.commit()
