from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), unique=True, nullable=False)
    age = db.Column(db.String(100), unique=False, nullable=False)
    weight = db.Column(db.String(100), unique=False, nullable=False)
    user = db.relationship("Favorite_character")

    def __repr__(self):
        return '<Characters %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
        }
    
class Favorite_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_character = db.Column(db.String(125), db.ForeignKey('characters.name'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __repr__(self):
        return '<Favorite_character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "favorite_character": self.favorite_character,
            "user_id": self.user_id,
        }

class Favorite_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_planet = db.Column(db.String(125), db.ForeignKey('planets.name'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __repr__(self):
        return '<Favorite_planet %r>' % self.id
    
    
    def serialize(self):
        return {
            "id": self.id,
            "favorite_planet": self.favorite_planet,
            "user_id": self.user_id,
        }
    