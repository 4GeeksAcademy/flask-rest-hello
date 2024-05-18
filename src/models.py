from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import ARRAY, TIMESTAMP
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    height = db.Column(db.Integer)
    homeworld = db.Column(db.String(250))
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    created = db.Column(TIMESTAMP, server_default=func.now(), nullable=False)
    edited = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
    url = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

    def serialize_single(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "homeworld": self.homeworld,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "created": self.created,
            "edited": self.edited,
            "url": self.url,
        }

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(250))
    diameter = db.Column(db.Numeric)
    gravity = db.Column(db.Numeric)
    created = db.Column(db.TIMESTAMP, server_default=func.now(), nullable=False)
    edited = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
    name = db.Column(db.String(250))
    orbital_period = db.Column(db.Integer)
    population = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    surface_water = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    url = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

    def serialize_single(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "created": self.created,
            "edited": self.edited,
            "url": self.url,
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class FavoritePerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
        }