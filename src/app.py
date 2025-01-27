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
from models import db, User
from peopleService import PeopleService
from planetService import PlanetService
from userService import UserService
from starshipService import StarshipService
from vehicleService import VehicleService
from specieService import SpecieService
from filmService import FilmService
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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/people", methods=["GET"])
def get_people_list():
    try:
        people_list = PeopleService().get_list()  

        if not people_list:  
            return jsonify({"message": "No people found"}), 400

        return jsonify(people_list), 200  

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/people/<int:people_id>", methods=["GET"])
def get_people(people_id):
    try:
        person = PeopleService().get_people(people_id)  
        if person is None: 
            return jsonify({"message": "Person not found"}), 404  

        return jsonify(person), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/planets", methods=["GET"])
def get_planet_list():
    try:
        planet_list = PlanetService().get_list()  

        if not planet_list:  
            return jsonify({"message": "No planet found"}), 400

        return jsonify(planet_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    try:
        planet = PlanetService().get_planet(planet_id)  
        if planet is None: 
            return jsonify({"message": "Planet not found"}), 404  

        return jsonify(planet), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route("/starships", methods=["GET"])
def get_starship_list():
    try:
        starship_list = StarshipService().get_list()  

        if not starship_list:  
            return jsonify({"message": "No starship found"}), 400

        return jsonify(starship_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/starship/<int:starship_id>", methods=["GET"])
def get_starship(starship_id):
    try:
        starship = StarshipService().get_starship(starship_id)  
        if starship is None: 
            return jsonify({"message": "starship not found"}), 404  

        return jsonify(starship), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/vehicles", methods=["GET"])
def get_vehicle_list():
    try:
        vehicle_list = VehicleService().get_list()  

        if not vehicle_list:  
            return jsonify({"message": "No vehicle found"}), 400

        return jsonify(vehicle_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route("/vehicle/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    try:
        vehicle = VehicleService().get_vehicle(vehicle_id)  
        if vehicle is None: 
            return jsonify({"message": "vehicle not found"}), 404  

        return jsonify(vehicle), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/species", methods=["GET"])
def get_specie_list():
    try:
        specie_list = SpecieService().get_list()  

        if not specie_list:  
            return jsonify({"message": "No specie found"}), 400

        return jsonify(specie_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
   


@app.route("/specie/<int:specie_id>", methods=["GET"])
def get_specie(specie_id):
    try:
        specie = SpecieService().get_specie(specie_id)  
        if specie is None: 
            return jsonify({"message": "specie not found"}), 404  

        return jsonify(specie), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/films", methods=["GET"])
def get_film_list():
    try:
        film_list = FilmService().get_list()  

        if not film_list:  
            return jsonify({"message": "No film found"}), 400

        return jsonify(film_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/film/<int:film_id>", methods=["GET"])
def get_film(film_id):
    try:
        film = FilmService().get_film(film_id)  
        if film is None: 
            return jsonify({"message": "film not found"}), 404  

        return jsonify(film), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['GET'])
def get_user_list():
    try:
        user_list = UserService().get_list()  

        if not user_list:  
            return jsonify({"message": "No users found"}), 400

        return jsonify(user_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = UserService().get_user(user_id)  
        if user is None: 
            return jsonify({"message": "user not found"}), 404  

        return jsonify(user), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorite_list(user_id):
    try:
        favorite_list = UserService().get_favorite_list(user_id)  
        if not favorite_list:  
            return jsonify({"message": "No Favorites found"}), 400

        return jsonify(favorite_list), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
