import pytest
from pytest_factoryboy import register

from project import create_app, db as _db
from project.tdd.factories import MemberFactory
from project.users.factories import UserFactory


register(UserFactory)
register(MemberFactory)


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def db(app):
    """
    https://github.com/pytest-dev/pytest-flask/issues/70
    """
    with app.app_context():
        _db.create_all()
        _db.session.commit()

        yield _db

        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def tmp_upload_dir(tmpdir, config):
    config.update(UPLOADS_DEFAULT_DEST=tmpdir.mkdir("tmp"))
