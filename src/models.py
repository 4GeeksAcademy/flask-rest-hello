from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

people_films = db.Table('people_films',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

people_vehicles = db.Table('people_vehicles',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True)
)

people_starships = db.Table('people_starships',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True)
)

planet_films = db.Table('planet_films',
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

film_starships = db.Table('film_starships',
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True)
)

vehicle_films = db.Table('vehicle_films',
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

specie_films = db.Table('specie_films',
    db.Column('specie_id', db.Integer, db.ForeignKey('specie.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

favorite_films = db.Table(
    'favorite_films',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id', ondelete='CASCADE'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id', ondelete='CASCADE'), primary_key=True)
)

favorite_people = db.Table(
    'favorite_people',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id', ondelete='CASCADE'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), primary_key=True)
)

favorite_starships = db.Table(
    'favorite_starships',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id', ondelete='CASCADE'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id', ondelete='CASCADE'), primary_key=True)
)

favorite_planets = db.Table(
    'favorite_planets',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id', ondelete='CASCADE'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id', ondelete='CASCADE'), primary_key=True)
)

favorite_species = db.Table(
    'favorite_species',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id', ondelete='CASCADE'), primary_key=True),
    db.Column('specie_id', db.Integer, db.ForeignKey('specie.id', ondelete='CASCADE'), primary_key=True)
)


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String, unique=False, nullable=False)
    skin_color = db.Column(db.String, unique=False, nullable=False)
    eye_color = db.Column(db.String, unique=False, nullable=False)
    birth_year = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=False)
    
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True) 
    homeworld = db.relationship('Planet', back_populates='residents')

    films = db.relationship('Film', secondary=people_films, back_populates='characters')
    
    species_id = db.Column(db.Integer, db.ForeignKey('specie.id'), nullable=True)  
    species = db.relationship('Specie', back_populates='people')

    vehicles = db.relationship('Vehicle', secondary=people_vehicles, back_populates='pilots')
    
    starships = db.relationship('Starship', secondary=people_starships, back_populates='pilots')

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "films": [film.title for film in self.films],
            "species": self.species.name if self.species else None, 
            "vehicles":  [vehicle.name for vehicle in self.vehicles],
            "starships":  [starship.name for starship in self.starships] 
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String, unique=False, nullable=False)
    terrain = db.Column(db.String, unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    
    residents = db.relationship('People', back_populates='homeworld')

    films = db.relationship('Film', secondary=planet_films, back_populates='planets')
    
    def __repr__(self):
        return f'<Planet {self.name}>'

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
            "residents": [resident.serialize() for resident in self.residents],
            "films": [film.title for film in self.films]
        }


class Starship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=True)
    length = db.Column(db.String, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.String, unique=False, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=True)
    passengers = db.Column(db.Integer, unique=False, nullable=True)
    cargo_capacity = db.Column(db.Integer, unique=False, nullable=True)
    consumables = db.Column(db.String, unique=False, nullable=True)
    starship_class = db.Column(db.String, unique=False, nullable=False)
    
    pilots = db.relationship('People', secondary=people_starships, back_populates='starships')  

    films = db.relationship('Film', secondary=film_starships, back_populates='starships')

    def __repr__(self):
        return f'<Starship {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "starship_class": self.starship_class,
            "pilots":[pilot.name for pilot in self.pilots],
            "films": [film.title for film in self.films],
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=True)
    length = db.Column(db.String, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.String, unique=False, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=True)
    passengers = db.Column(db.Integer, unique=False, nullable=True)
    cargo_capacity = db.Column(db.Integer, unique=False, nullable=True)
    consumables = db.Column(db.String, unique=False, nullable=True)
    vehicle_class = db.Column(db.String, unique=False, nullable=False)
    
    pilots = db.relationship('People', secondary=people_vehicles, back_populates='vehicles')

    films = db.relationship('Film', secondary=vehicle_films, back_populates='vehicles')

    def __repr__(self):
        return f'<Vehicle {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class,
            "pilots": [pilot.name for pilot in self.pilots],
            "films": [film.title for film in self.films]
        }
    

class Specie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    classification = db.Column(db.String, unique=False, nullable=False)
    designation = db.Column(db.String, unique=False, nullable=False)
    average_height = db.Column(db.Integer, unique=False, nullable=False)
    skin_colors = db.Column(db.String, unique=False, nullable=False)
    hair_colors = db.Column(db.String, unique=False, nullable=False)
    eye_colors = db.Column(db.String, unique=False, nullable=True)
    average_lifespan = db.Column(db.Integer, unique=False, nullable=True)
    homeworld = db.Column(db.String, unique=False, nullable=True)
    language = db.Column(db.String, unique=False, nullable=False)
    
    people = db.relationship('People', back_populates='species')

    films = db.relationship('Film', secondary=specie_films, back_populates='species')

    def __repr__(self):
        return f'<Specie {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "skin_colors": self.skin_colors,
            "hair_colors": self.hair_colors,
            "eye_colors": self.eye_colors,
            "average_lifespan": self.average_lifespan,
            "homeworld": self.homeworld,
            "language": self.language,
            "people": [people.serialize() for people in self.people],
            "films": [film.title for film in self.films]
        }
    

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    episode_id = db.Column(db.Integer, unique=False, nullable=False)
    opening_crawl = db.Column(db.String, unique=False, nullable=False)
    director = db.Column(db.String, unique=False, nullable=False)
    producer = db.Column(db.String, unique=False, nullable=False)
    release_date = db.Column(db.String, unique=False, nullable=False)
    
    characters = db.relationship('People', secondary=people_films, back_populates='films')

    planets = db.relationship('Planet', secondary=planet_films, back_populates='films')

    starships = db.relationship('Starship', secondary=film_starships, back_populates='films')

    vehicles = db.relationship('Vehicle', secondary=vehicle_films, back_populates='films')
    
    species = db.relationship('Specie', secondary=specie_films, back_populates='films')

    def __repr__(self):
        return f'<Film {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date,
            "characters": [character.name for character in self.characters],
            "planets": [planet.name for planet in self.planets],
            "starships":[starship.name for starship in self.starships], 
            "vehicles": [vehicle.name for vehicle in self.vehicles],
            "species": [specie.name for specie in self.species]
        }
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='favorites')

    films = db.relationship('Film', secondary=favorite_films, lazy='subquery')
    people = db.relationship('People', secondary=favorite_people, lazy='subquery')
    starships = db.relationship('Starship', secondary=favorite_starships, lazy='subquery')
    planets = db.relationship('Planet', secondary=favorite_planets, lazy='subquery')
    species = db.relationship('Specie', secondary=favorite_species, lazy='subquery')


    def __repr__(self):
        return f'<Favorite {self.user_id} - Favorites>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "films": [film.serialize() for film in self.films],
            "people": [people.serialize() for people in self.people],
            "starships": [starship.serialize() for starship in self.starships],
            "planets": [planet.serialize() for planet in self.planets],
            "species": [specie.serialize() for specie in self.species],
            
            
        }
class prueba:
    def algo(self):
        return "algo"

    