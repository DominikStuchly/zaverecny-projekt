# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Auto(db.Model):
    __tablename__ = 'auto'
    id = db.Column(db.Integer, primary_key=True )
    plate = db.Column(db.String, nullable=False, index=False)
    confidence = db.Column(db.Float, nullable=False, index=True)
    processing_time_ms = db.Column(db.Float)
    image=db.Column(db.LargeBinary)
    region = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime)
    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

