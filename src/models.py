from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
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
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_people = db.Column(db.Integer(), db.ForeignKey(People.id))
    id_planets = db.Column(db.Integer(), db.ForeignKey(Planets.id))
    id_users = db.Column(db.Integer(), db.ForeignKey(User.id))

    def __repr__(self):
        return '<Planets %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
        }
