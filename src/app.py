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
from models import db, Usuario, Planeta, Personaje, Vehiculo, PlanetaFavorito, PersonajeFavorito
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

@app.route('/users', methods=['GET'])
def get_users():
    response = Usuario.query.all()
    return jsonify(response), 200

@app.route('/users/favorites', method=['GET'])
def get_favorites():
    user_id = Usuario.query.get(Usuario.id)

    if not user_id:
        return jsonify({"error": "User not found"}), 404

    favorites = {
        "planetas": [p.serialize() for p in Usuario.planetas_favoritos],
        "personajes": [p.serialize() for p in Usuario.personajes_favoritos],
        "vehiculos": [v.serialize() for v in Usuario.vehiculos_favoritos],
    }

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', method=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = PlanetaFavorito.query.filter_by(usuario_id=user_id, planeta_id=planet_id).first()

    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = PlanetaFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([fav.serialize() for fav in updated_favorites]), 200

@app.route('/favorite/people/<int:people_id>', method=['DELETE'])
def delete_fav_person(people_id):
    user_id = Usuario.query.get(Usuario.id)
    person = PersonajeFavorito.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()

    if not person:
        return jsonify({"message": "Person not found"}), 404

    db.session.delete(person)
    db.session.commit()

    updated_people = PersonajeFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_people]), 200

@app.route('/planets/<int:planet_id>', method=['DELETE'])
def delete_planet(planet_id):
    planet = Planeta.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()

    if not person:
        return jsonify({"message": "Person not found"}), 404

    db.session.delete(person)
    db.session.commit()

    updated_people = PersonajeFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_people]), 200

@app.route('/people', method=['DELETE'])
def delete_fav_person(people_id):
    user_id = Usuario.query.get(Usuario.id)
    person = PersonajeFavorito.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()

    if not person:
        return jsonify({"message": "Person not found"}), 404

    db.session.delete(person)
    db.session.commit()

    updated_people = PersonajeFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_people]), 200

@app.route('/')
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
