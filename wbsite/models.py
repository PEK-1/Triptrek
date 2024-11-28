from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    trips = db.relationship('Trip', backref='user', lazy=True)
    map_data = db.relationship('MapData', backref='user', lazy=True)  

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User model
    place = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Float, nullable=True)
    accommodation = db.Column(db.String(100), nullable=True)
    transport = db.Column(db.String(50), nullable=True)
    local_travel = db.Column(db.String(50), nullable=True)
    places_visited = db.Column(db.Text, nullable=True)
    food_recommendations = db.Column(db.Text, nullable=True)
    trip_description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class MapData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User model
    country = db.Column(db.String(100), nullable=False)  # Country name
    color = db.Column(db.String(20), default='white')  # Selected color for the country
    note = db.Column(db.String(255), nullable=True)  # Note for the country
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())  # Automatically updates on modification
