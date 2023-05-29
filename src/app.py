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
from models import db, Users, Favourites_people, People, Vehicles, Favourites_vehicles, Favourites_planets, Planets

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


# GET ALL ENDPOINTS

# USERS

@app.route('/users', methods=['GET'])
def users_get_all():
    users = list(map(lambda item: item.serialize(), Users.query.all()))

    response_body = {
        "msg": "ok",
        "response": users
    }

    return jsonify(response_body), 200


@app.route('/users/<int:id>', methods=['GET'])
def users_get_one(id):
    user = Users.query.filter_by(id=id).first().serialize()

    response_body = {
        "msg": "ok",
        "response": user
    }

    return jsonify(response_body), 200

# PEOPLE


@app.route('/people', methods=['GET'])
def people_get_all():
    people = list(map(lambda item: item.serialize(), People.query.all()))

    response_body = {
        "msg": "ok",
        "response": people
    }

    return jsonify(response_body), 200


@app.route('/people/<int:id>', methods=['GET'])
def people_get_one(id):

    response_body = {}
    person = People.query.filter_by(id=id).first()

    if favourites == None:
        response_body["msg"]=f"User with id {id} doesn't exist"
        return jsonify(response_body), 404

    response_body["msg"]="Ok"
    return jsonify(response_body), 200


# VEHICLES

@app.route('/vehicles', methods=['GET'])
def vehicles_get_all():
    vehicles = list(map(lambda item: item.serialize(), Vehicles.query.all()))

    response_body = {
        "msg": "ok",
        "response": vehicles
    }

    return jsonify(response_body), 200


@app.route('/vehicles/<int:id>', methods=['GET'])
def vehicles_get_one(id):
    vehicle = Vehicles.query.filter_by(id=id).first().serialize()

    response_body = {
        "msg": "ok",
        "response": vehicle
    }

    return jsonify(response_body), 200


# PLANETS

@app.route('/planets', methods=['GET'])
def planets_get_all():
    planets = list(map(lambda item: item.serialize(), Planets.query.all()))

    response_body = {
        "msg": "ok",
        "response": planets
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:id>', methods=['GET'])
def planets_get_one(id):
    planet = Planets.query.filter_by(id=id).first().serialize()

    response_body = {
        "msg": "ok",
        "response": planet
    }

    return jsonify(response_body), 200


# POST PEOPLE
@app.route('/people', methods=['POST'])
def people_post():

    response_body = {}

    r = request.get_json(force=True)

    # Filters
    if r is None:
        response_body["msg"] = "The request body is null"
        return jsonify(response_body), 400

    if not "name" in r:
        response_body["msg"] = "Name not found"
        return jsonify(response_body), 400

    if not "mass" in r:
        response_body["msg"] = "Mass not found"
        return jsonify(response_body), 400
    
    if not "height" in r:
        response_body["msg"] = "Height not found"
        return jsonify(response_body), 400
    
    if not "hair_color" in r:
        response_body["msg"] = "Hair color not found"
        return jsonify(response_body), 400
    
    if not "gender" in r:
        response_body["msg"] = "Gender not found"
        return jsonify(response_body), 400
    
    if not "eye_color" in r:
        response_body["msg"] = "Eye color not found"
        return jsonify(response_body), 400
    
    if not "birth_year" in r:
        response_body["msg"] = "Birth year not found"
        return jsonify(response_body), 400
    

    filter_name = People.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = "Name must be unique"
        return jsonify(response_body), 400
    # Filters End

    person = People(name=r["name"], gender=r["gender"], birth_year=r["birth_year"],
                    eye_color=r["eye_color"], hair_color=r["hair_color"], mass=r["mass"], height=r["height"])

    db.session.add(person)
    db.session.commit()

    response_body["msg"] = "ok"
    return jsonify(response_body), 200

# POST VEHICLES
@app.route('/vehicles', methods=['POST'])
def vehicles_post():

    response_body = {}

    r = request.get_json(force=True)

    # Filters
    if r is None:
        return "The request body is null", 400

    if not "name" in r:
        response_body["msg"] = "Name not found"
        return jsonify(response_body), 400

    if not "cargo_capacity" in r:
        response_body["msg"] = "Cargo Capacity not found"
        return jsonify(response_body), 400
    
    if not "consumables" in r:
        response_body["msg"] = "Consumables not found"
        return jsonify(response_body), 400
    
    if not "cost_in_credits" in r:
        response_body["msg"] = "Cost in credits color not found"
        return jsonify(response_body), 400
    
    if not "crew" in r:
        response_body["msg"] = "Crew not found"
        return jsonify(response_body), 400
    
    if not "length" in r:
        response_body["msg"] = "Length color not found"
        return jsonify(response_body), 400
    
    if not "manufacturer" in r:
        response_body["msg"] = "Manufacturer year not found"
        return jsonify(response_body), 400

    if not "max_atmosphering_speed" in r:
        response_body["msg"] = "Max atmosphering speed year not found"
        return jsonify(response_body), 400
    
    if not "manufacturer" in r:
        response_body["msg"] = "Model year not found"
        return jsonify(response_body), 400
    
    if not "manufacturer" in r:
        response_body["msg"] = "Passengers year not found"
        return jsonify(response_body), 400
    
    if not "manufacturer" in r:
        response_body["msg"] = "Vehicle class year not found"
        return jsonify(response_body), 400
    

    filter_name = Vehicles.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = "Name must be unique"
        return jsonify(response_body), 400
    # Filters End

    vehicle = Vehicles(name=r["name"], model=r["model"], vehicle_class=r["vehicle_class"],
                    manufacturer=r["manufacturer"], cost_in_credits=r["cost_in_credits"], 
                    length=r["length"], crew=r["crew"], passengers=r["passengers"], 
                    max_atmosphering_speed=r["max_atmosphering_speed"], 
                    cargo_capacity=r["cargo_capacity"], consumables=r["consumables"])

    db.session.add(vehicle)
    db.session.commit()

    response_body["msg"] = "ok"
    return jsonify(response_body), 200


# POST VEHICLES
@app.route('/planets', methods=['POST'])
def planets_post():

    response_body = {}

    r = request.get_json(force=True)

    # Filters
    if r is  None:
        return "The request body is null", 400

    if not "name" in r:
        response_body["msg"] = "Name not found"
        return jsonify(response_body), 400

    if not "climate" in r:
        response_body["msg"] = "Climate not found"
        return jsonify(response_body), 400
    
    if not "diameter" in r:
        response_body["msg"] = "Diameter not found"
        return jsonify(response_body), 400
    
    if not "gravity" in r:
        response_body["msg"] = "Gravity in credits color not found"
        return jsonify(response_body), 400
    
    if not "orbital_period" in r:
        response_body["msg"] = "Orbital period not found"
        return jsonify(response_body), 400
    
    if not "population" in r:
        response_body["msg"] = "Population color not found"
        return jsonify(response_body), 400
    
    if not "rotation_period" in r:
        response_body["msg"] = "Rotation period year not found"
        return jsonify(response_body), 400

    if not "surface_water" in r:
        response_body["msg"] = "Surface water speed year not found"
        return jsonify(response_body), 400
    
    if not "terrain" in r:
        response_body["msg"] = "Terrain year not found"
        return jsonify(response_body), 400
    

    filter_name = Planets.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = "Name must be unique"
        return jsonify(response_body), 400
    # Filters End

    planet = Planets(name=r["name"], climate=r["climate"], diameter=r["diameter"],
                    gravity=r["gravity"], orbital_period=r["orbital_period"], 
                     population=r["population"], rotation_period=r["rotation_period"], 
                    surface_water=r["surface_water"], terrain=r["terrain"])

    db.session.add(planet)
    db.session.commit()

    response_body["msg"] = "ok"
    return jsonify(response_body), 200


# DELETE PEOPLE

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):  
    response_body = {}

    person = People.query.get(id)

    if person == None:
        response_body["msg"] = f"Person with id {id} doesn't exist"
        return jsonify(response_body), 400

    db.session.delete(person)
    db.session.commit()
    
    response_body["msg"] = "Ok"
    return jsonify(response_body), 200

# DELETE VEHICLES

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicles(id):  
    response_body = {}

    vehicle = Vehicles.query.get(id)

    if vehicle == None:
        response_body["msg"] = f"Vehicle with id {id} doesn't exist"
        return jsonify(response_body), 400

    db.session.delete(vehicle)
    db.session.commit()
    
    response_body["msg"] = "Ok"
    return jsonify(response_body), 200

# DELETE PLANETS

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planets(id):  
    response_body = {}

    planet = People.query.get(id)

    if planet == None:
        response_body["msg"] = f"Planet with id {id} doesn't exist"
        return jsonify(response_body), 400

    db.session.delete(planet)
    db.session.commit()
    
    response_body["msg"] = "Ok"
    return jsonify(response_body), 200


# MODIFY PEOPLE
@app.route('/people/<int:id>', methods=['PUT'])
def modify_people(id):  
    response_body = {}

    r = request.get_json(force=True)
    person = People.query.get(id)

    if person == None:
        response_body["msg"] = f"Person with id {id} doesn't exist"
        return jsonify(response_body), 400
    
    filter_name = People.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = f"Name {r['name']} already exist"
        return jsonify(response_body), 400

    if "name" in r:
        person.name = r["name"] 
    
    if "birth_year" in r:
        person.birth_year = r["birth_year"]
        
    if "eye_color" in r:
        person.eye_color = r["eye_color"]
    
    if "gender" in r:
        person.gender = r["gender"]
    
    if "hair_color" in r:
        person.hair_color = r["hair_color"]
    
    if "height" in r:
        person.height = r["height"]
    
    if "mass" in r:
        person.mass = r["mass"]
    
    db.session.commit()

    response_body["msg"] = "Ok"
    return jsonify(response_body), 200


# MODIFY VEHICLES
@app.route('/vehicles/<int:id>', methods=['PUT'])
def modify_vehicles(id):  
    response_body = {}

    r = request.get_json(force=True)
    vehicle = Vehicles.query.get(id)

    if vehicle == None:
        response_body["msg"] = f"Vehicle with id {id} doesn't exist"
        return jsonify(response_body), 400
    
    filter_name = Vehicles.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = f"Name {r['name']} already exist"
        return jsonify(response_body), 400

    if "name" in r:
        vehicle.name = r["name"] 
    
    if "cargo_capacity" in r:
        vehicle.cargo_capacity = r["cargo_capacity"]
        
    if "consumables" in r:
        vehicle.consumables = r["consumables"]
    
    if "cost_in_credits" in r:
        vehicle.cost_in_credits = r["cost_in_credits"]
    
    if "crew" in r:
        vehicle.crew = r["crew"]
    
    if "length" in r:
        vehicle.length = r["length"]
    
    if "manufacturer" in r:
        vehicle.manufacturer = r["manufacturer"]
    
    if "max_atmosphering_speed" in r:
        vehicle.max_atmosphering_speed = r["max_atmosphering_speed"]
    
    if "model" in r:
        vehicle.model = r["model"]
    
    if "passengers" in r:
        vehicle.passengers = r["passengers"]
    
    if "vehicle_class" in r:
        vehicle.vehicle_class = r["vehicle_class"]
    
    db.session.commit()

    response_body["msg"] = "Ok"
    return jsonify(response_body), 200

# MODIFY PLANETS
@app.route('/planets/<int:id>', methods=['PUT'])
def modify_planets(id):  
    response_body = {}

    r = request.get_json(force=True)
    planet = Planets.query.get(id)

    if planet == None:
        response_body["msg"] = f"Planet with id {id} doesn't exist"
        return jsonify(response_body), 400
    
    filter_name = Planets.query.filter_by(name=r["name"]).first()  # Check unique name
    if filter_name != None:
        response_body["msg"] = f"Name {r['name']} already exist"
        return jsonify(response_body), 400

    if "name" in r:
        planet.name = r["name"] 
    
    if "climate" in r:
        planet.climate = r["climate"]
        
    if "diameter" in r:
        planet.diameter = r["diameter"]
    
    if "gravity" in r:
        planet.gravity = r["gravity"]
    
    if "orbital_period" in r:
        planet.orbital_period = r["orbital_period"]
    
    if "population" in r:
        planet.population = r["population"]
    
    if "rotation_period" in r:
        planet.rotation_period = r["rotation_period"]
    
    if "surface_water" in r:
        planet.surface_water = r["surface_water"]
    
    if "terrain" in r:
        planet.terrain = r["terrain"]
    
    db.session.commit()

    response_body["msg"] = "Ok"
    return jsonify(response_body), 200

# GET USER FAVOURITES
@app.route('/users/favorites/<int:id>', methods=['GET'])
def get_favourites(id):
    response_body = {}

    favourites_people = list(map(lambda item: item.serialize(),Favourites_people.query.filter_by(user_id=id).all()))  
    favourites_vehicles = list(map(lambda item: item.serialize(),Favourites_vehicles.query.filter_by(user_id=id).all()))
    favourites_planets = list(map(lambda item: item.serialize(),Favourites_planets.query.filter_by(user_id=id).all()))

    favourites = []

    if favourites_people:
        favourites = [*favourites,*favourites_people]
        
    if favourites_vehicles:
        favourites = [*favourites,*favourites_vehicles]
    
    if favourites_planets:
        favourites = [*favourites,*favourites_planets]

    response_body["msg"] = "Ok"
    response_body["response"] = favourites
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
