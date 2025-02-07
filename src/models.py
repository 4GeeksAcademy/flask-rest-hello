from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy import ForeignKey

db = SQLAlchemy()

@dataclass
class Users(db.Model):
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name: str = db.Column(db.String(50), nullable=False)
    password = db.Column(db.VARCHAR(60), nullable=False)
    email: str = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.user_name}>'

class FavouriteType (str,Enum):
    characters = "characters"
    planets = "planets"
    starships = "starships"

@dataclass
class Favourites(db.Model):
    __tablename__ = 'favourites'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    external_id: int = db.Column(db.Integer, nullable=False)
    type: str = db.Column(db.Enum(FavouriteType), nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Favourite {self.name}>'

@dataclass
class Characters(db.Model):
    __tablename__ = 'characters'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    height: int = db.Column(db.Integer, nullable=False)
    home_world: int = db.Column(db.Integer, ForeignKey('planets.id'), nullable=False)
    mass: int = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Character {self.name}>'

@dataclass
class Starships(db.Model):
    __tablename__ = 'starships'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    cost_in_credits: int = db.Column(db.Integer, nullable=False)
    crew: str = db.Column(db.String(5000), nullable=False)
    passengers: str = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Starship {self.name}>'

@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    diameter: int = db.Column(db.Integer, nullable=False)
    population: int = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'
