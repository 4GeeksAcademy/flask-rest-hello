from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

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
        return '<Planets %r>' % self.name

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

    def __repr__(self):
        return '<Characters %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
        }
    
class Favorite_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_character = db.Column(db.Integer, db.ForeignKey('characters.id'), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    user = db.relationship("User", backref = db.backref('favorite_character', lazy=True))
    character = db.relationship("Characters", backref = db.backref('favorite_character', lazy=True))

    def __repr__(self):
        return '<Favorite_character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.favorite_character,
            "user_id": self.user_id,
        }

class Favorite_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_planet = db.Column(db.Integer, db.ForeignKey('planets.id'), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    user = db.relationship("User", backref = db.backref('favorite_planet', lazy=True))
    planet = db.relationship("Planets", backref = db.backref('favorite_planet', lazy=True))
    

    def __repr__(self):
        return '<Favorite_planet %r>' % self.id
    
    
    def serialize(self):
        return {
            "id": self.id,
            "favorite_planet": self.favorite_planet,
            "user_id": self.user_id,
        }
    