from flask_sqlalchemy import SQLAlchemy

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
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    heigth = db.Column(db.String(50), nullable=True)
    mass = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<People {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.heigth,
            "mass": self.mass,
            "gender": self.gender
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Planet {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_type = db.Column(db.String(50), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Favorite user_id={self.user_id}, favorite_type={self.favorite_type}, favorite_id={self.favorite_id}'
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "favorite_type": self.favorite_type,
            "favorite_id": self.favorite_id
        }