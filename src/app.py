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
from models import db, User, People, Favorite, Planets
from sqlalchemy import select
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


@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    if len(users) == 0:
        return jsonify({
            "msg": "No se encontraron los resultados"
        }), 404
    else:
        return jsonify([user.serialize() for user in users]), 200


@app.route("/people", methods=["GET"])
def get_people():
    characters = People.query.all()
    if len(characters) == 0:
        return jsonify({
            "msg": "No se encontraron los resultados"
        }), 404
    else:
        return jsonify([character.serialize_people() for character in characters]), 200


@app.route('/people/<int:id>', methods=["GET"])
def get_character(id):
    character = People.query.filter_by(id=id).first()
    if character is None:
        return jsonify({
            "msg": "No se encontraron los resultados"
        }), 404
    else:
        return jsonify({
            "character": character.serialize_people()
        }), 200


@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    if len(planets) == 0:
        return jsonify({
            "msg": "No se encontraron los resultados"
        }), 404
    else:
        return jsonify([planet.serialize_planets() for planet in planets]), 200


@app.route("/planets/<int:id>", methods=["GET"])
def get_planet(id):
    planet = Planets.query.filter_by(id=id).first()

    if planet is None:
        return jsonify({
            "msg": "No se encontro el recurso"
        }), 404
    else:
        return jsonify(planet.serialize_planets()), 200


@app.route("/favorites/user/", methods=["GET"])
def favorites_user():
    favorites = Favorite.query.filter_by(user_id=1).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def post_favorite_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({
            "msg": "Not found"
        }), 404
    favorite = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if favorite:
        return jsonify({
            "msg": "Already exist"
        }), 409
    new_favorite = Favorite(user_id=1, planet_id=planet_id, people_id=None)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def post_favorite_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        return jsonify({
            "msg": "Not found"
        }), 404
    favorite = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if favorite:
        return jsonify({
            "msg": "Already exist"
        }), 409

    new_favorite = Favorite(user_id=1, people_id=people_id, planet_id=None)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize())


@app.route("/favorite/planet/<int:id>", methods=["DELETE"])
def delete_favorite_planet(id):
    favorite = Favorite.query.filter_by(user_id=1, planet_id=id).first()
    if favorite is None:
        return jsonify({
            "msg": "Not found"
        }), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({
        "msg": "Successfully deleted"
    }), 200


@app.route("/favorite/people/<int:id>", methods=["DELETE"])
def delete_favorite_people(id):
    favorite = Favorite.query.filter_by(user_id=1, people_id=id).first()
    if favorite is None:
        return jsonify({
            "msg": "Not found"
        }), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({
        "msg": "Successfully deleted"
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
