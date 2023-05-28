from flask_sqlalchemy import SQLAlchemy
# from eralchemy2 import render_er

db = SQLAlchemy()


class Users(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False)
    last_name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    favourites_people = db.relationship(
        "Favourites_people", backref='users', lazy=True)
    favourites_vehicles = db.relationship(
        "Favourites_vehicles", backref='users', lazy=True)
    favourites_planets = db.relationship(
        "Favourites_planets", backref='users', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }


class People(db.Model):

    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_year = db.Column(db.String(10), nullable=False)
    eye_color = db.Column(db.String(10), nullable=False)
    hair_color = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    favourites_persons = db.relationship(
        "Favourites_people", backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "mass": self.mass,
            "height": self.height,
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(20), nullable=False)
    vehicle_class = db.Column(db.String(20), nullable=False)
    manufacturer = db.Column(db.String(20), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(20), nullable=False)

    favourites_vehicles = db.relationship(
        "Favourites_vehicles", backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), unique=True, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(20), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(20), nullable=False)
    terrain = db.Column(db.String(20), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)

    favourites_planets = db.relationship(
        "Favourites_planets", backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }


# FAVOURITES


class Favourites_people(db.Model):
    __tablename__ = 'favourites_people'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'people.id'), nullable=False)

    def __repr__(self):
        return '<Favourites_people %r>' % self.id

    def serialize(self):
        person = People.query.filter_by(id=self.person_id).first()
        user = Users.query.filter_by(id=self.user_id).first()

        return {
            "id": self.id,
            "user_info": user.serialize(),
            "person_info": person.serialize()
        }


class Favourites_vehicles(db.Model):
    __tablename__ = 'favourites_vehicles'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicles_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id'), nullable=False)

    def __repr__(self):
        return '<Favourites_vehicles %r>' % self.id

    def serialize(self):
        vehicle = Vehicles.query.filter_by(id=self.vehicles_id).first()
        user = Users.query.filter_by(id=self.user_id).first()

        return {
            "id": self.id,
            "user_info": user.serialize(),
            "vehicle_info": vehicle.serialize()
        }


class Favourites_planets(db.Model):
    __tablename__ = 'favourites_planets'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey(
        'planets.id'), nullable=False)

    def __repr__(self):
        return '<Favourites_planets %r>' % self.id

    def serialize(self):
        planet = Planets.query.filter_by(id=self.planets_id).first()
        user = Users.query.filter_by(id=self.user_id).first()

        return {
            "id": self.id,
            "user_info": user.serialize(),
            "planet_info": planet.serialize()
        }

 # render_er(db.Model, 'diagram.png')
