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

from flask_login import LoginManager
login_manager = LoginManager()
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

login_manager.init_app(app)

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


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
    person = People.query.filter_by(id=id).first().serialize()

    response_body = {
        "msg": "ok",
        "response": person
    }

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

# PUT, POST, DELETE => PLANETS, PEOPLE, VEHICLES


@app.route('/people/post', methods=['POST'])
def people_post():

    response_body = {}

    r = request.get_json(force=True)

    filter_name = People.query.filter_by(name=r["name"]).first()
    if filter_name != None:
        response_body["msg"] = "Name must be unique"
        return jsonify(response_body), 400

    person = People(name=r["name"], gender=r["gender"], birth_year=r["birth_year"],
                    eye_color=r["eye_color"], hair_color=r["hair_color"], mass=r["mass"], height=r["height"])

    db.session.add(person)
    db.session.commit()

    response_body["msg"] = "ok"
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
