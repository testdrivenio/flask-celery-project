import os

from flask import current_app
from PIL import Image

from project.tdd.tasks import generate_avatar_thumbnail


def test_task_generate_avatar_thumbnail(db, member):
    # init state
    assert member.avatar
    assert not member.avatar_thumbnail

    generate_avatar_thumbnail(member.id)

    db.session.refresh(member)

    assert member.avatar_thumbnail

    thumbnail_full_path = os.path.join(
        current_app.config['UPLOADS_DEFAULT_DEST'],
        member.avatar_thumbnail
    )
    im = Image.open(thumbnail_full_path)

    assert im.height == 100
    assert im.width == 100
