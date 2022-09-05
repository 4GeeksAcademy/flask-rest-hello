from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))


    def __repr__(self):
        return f"<Favorites id={self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "people_id": self.people_id,
            "people_name": self.people_name,
            "planet_id": self.planet_id,
            "planet_name": self.planet_name
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10))
    birthday_year = db.Column(db.String(10))
    color_eyes = db.Column(db.String(10))
    height = db.Column(db.String(5))
    mass = db.Column(db.String(5))

    def __repr__(self):
        return f"<People id={self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birthday_year": self.birthday_year,
            "color_eyes": self.color_eyes,
            "height": self.height,
            "mass": self.mass
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    gravity = db.Column(db.String(10))
    terrain = db.Column(db.String(10))
    diametrer = db.Column(db.String(10))
    rotation_period = db.Column(db.String(10))
    orbital_period = db.Column(db.String(10))

    def __repr__(self):
        return f"<Planet id={self.id} name= {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "diametrer": self.diametrer,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period
        }

