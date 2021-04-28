from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database.'

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.Numeric(precision=4))
    color = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, year, color, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.user_token = user_token

    def __repr__(self):
        return f'The following car has been added to your collection: {self.year} {self.make} {self.model}'

    def set_id(self):
        return secrets.token_urlsafe()

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'color']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)