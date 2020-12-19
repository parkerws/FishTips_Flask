from datetime import datetime
from time import time
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(8), index=True, unique=True)
    state = db.Column(db.String(3))
    name = db.Column(db.String(64))
    timezone = db.Column(db.String(5))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)

    def __init__(self, station_id, state, name, timezone, lat, long):
        self.station_id = station_id
        self.state = state
        self.name = name
        self.timezone = timezone
        self.lat = lat
        self.long = long

    def __repr__(self):
        return '<Station {}, location {}>'.format(self.station_id, str(self.lat) +' '+ str(self.long))

    def serialize(self):
        return {
            "station_id": self.station_id,
            "state": self.state,
            "name": self.name,
            "timezone": self.timezone,
            "lat": self.lat,
            "long": self.long
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    