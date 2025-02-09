"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicles, Species, Films, Spaceships, Planets, Favourites, FavouritesType
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route ('/')
def sitemap():
    return generate_sitemap(app)

tables = {
    "species" : Species,
    "films" : Films,
    "planets" : Planets,
    "people" : People,
    "spaceships" : Spaceships,
    "vehicles" : Vehicles,
}

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    return jsonify(planets), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet) if planet else (jsonify({"error": "Planet not found"}), 404)

@app.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    return jsonify(people), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_character(people_id):
    character = People.query.get(people_id)
    return jsonify(character) if character else (jsonify({"error": "Character not found"}), 404)

@app.route("/films", methods=["GET"])
def get_films():
    films = Films.query.all()
    return jsonify(films), 200

@app.route("/films/<int:film_id>", methods=["GET"])
def get_film(film_id):
    film = Films.query.get(film_id)
    return jsonify(film) if film else (jsonify({"error": "Film not found"}), 404)

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify(vehicles), 200

@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    return jsonify(vehicle) if vehicle else (jsonify({"error": "Vehicle not found"}), 404)

@app.route("/spaceships", methods=["GET"])
def get_spaceships():
    spaceships = Spaceships.query.all()
    return jsonify(spaceships), 200

@app.route("/spaceships/<int:spaceship_id>", methods=["GET"])
def get_spaceship(spaceship_id):
    spaceship = Spaceships.query.get(spaceship_id)
    return jsonify(spaceship) if spaceship else (jsonify({"error": "Starship not found"}), 404)

@app.route("/species", methods=["GET"])
def get_species():
    species = Species.query.all()
    return jsonify(species), 200

@app.route("/species/<int:specie_id>", methods=["GET"])
def get_specie(specie_id):
    specie = Species.query.get(specie_id)
    return jsonify(specie) if specie else (jsonify({"error": "Specie not found, haber estudiao"}), 404)

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(users), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user) if user else (jsonify({"error": " User not found, haber estudiao"}), 404)

@app.route("/users/<int:user_id>/favs", methods=["GET", "POST", "DELETE"])
def handle_favs(user_id):

    if request.methods == "GET":
        favs = Favourites.query.filter_by(user_id=user_id).all()
        return jsonify(favs), 200
    
    data = request.get_json()

    if request.methods == "POST":
        required_fields = ["type", "external_id", "name"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    if not (data["type"] in FavouritesType._members_):
        return jsonify({"error": "Type not valid"}), 400
    if Favourites.query.filter_by(external_id=data["external_id"], user_id=user_id, type=data["type"]):
        return jsonify({"error": "Resource already faved"}), 400
    if not tables[data["type"]].query.filter_by(id=data["external_id"]).first():
        return jsonify({"error": "Resource not found"}), 400
    
    new_fav = Favourites(
        external_id=data["external_id"],
        type=data["type"],
        name=data["name"],
        user_id=user_id,
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav), 201

@app.route("/users/<int:user_id>/favs", methods=["DELETE"])
def delete_favs(user_id):
    required_fields = ["id"]
    
    data = request.get_json()
    if not all(field in data for field in required_fields):
      return jsonify({"error": "Missing required fields"}), 400
    
    fav = Favourites.query.filter_by(
        id=data["id"], user_id=user_id
    ).first()

    if not fav:
        return jsonify({"error": "Fav not found"}), 400
    
    db.session.delete(fav)
    db.session.commit()

    return jsonify(fav), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
