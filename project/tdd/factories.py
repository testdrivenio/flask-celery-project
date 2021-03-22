import os

import factory
from factory import LazyAttribute
from factory.fuzzy import FuzzyText
from flask import current_app
from PIL import Image

from project import db
from project.tdd.models import Member


class MemberFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Member
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ('username',)
        sqlalchemy_session_persistence = "commit"

    username = FuzzyText(length=6)
    email = LazyAttribute(lambda o: '%s@example.com' % o.username)

    @factory.lazy_attribute
    def avatar(self):

        width = 300
        height = 300
        color = 'blue'
        image_format = 'JPEG'
        image_palette = 'RGB'

        with Image.new(image_palette, (width, height), color) as thumb:
            filename = f'{self.username}.jpg'
            full_path = os.path.join(
                current_app.config['UPLOADS_DEFAULT_DEST'],
                filename
            )
            thumb.save(full_path, format=image_format)

        return filename
