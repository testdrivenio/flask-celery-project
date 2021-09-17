from project import db


class Member(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

    avatar = db.Column(db.String(256), nullable=False)
    avatar_thumbnail = db.Column(db.String(256), nullable=True)
