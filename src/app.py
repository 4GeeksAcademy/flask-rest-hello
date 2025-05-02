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
from models import db, Personaje, Usuario, Planeta, Vehiculo, PlanetaFavorito, PersonajeFavorito, VehiculoFavorito

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

@app.route('/people', methods=['GET'])
def get_people():
    people = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)
    return jsonify(personaje.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)
    return jsonify(planeta.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    response = Usuario.query.all()
    return jsonify(response), 200

@app.route('/users/favorites', method=['GET'])
def get_favorites():
    user = Usuario.query.get(Usuario.id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = {
        "planetas": [p.serialize() for p in Usuario.planetas_favoritos],
        "personajes": [p.serialize() for p in Usuario.personajes_favoritos],
        "vehiculos": [v.serialize() for v in Usuario.vehiculos_favoritos],
    }

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', method=['POST'])
def add_favorite_planet(planet_id):
    user = Usuario.query.get(Usuario.id)
    planeta = Planeta.query.get(planet_id)

    if not planeta:
        return jsonify({'error': 'Planeta no encontrado'}), 404
    
    favorito_existente= next((fav for fav in user.planetas_favoritos if fav.planeta_id == planet_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El planeta ya está en favoritos'}), 400
    nuevo_favorito = PlanetaFavorito(usuario_id=user.id, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Planeta añadido a favoritos', 'planeta': planeta.nombre}), 201

@app.route('/favorite/people/<int:people_id>', method=['POST'])
def add_favorite_personaje(people_id):
    user = Usuario.query.get(Usuario.id)
    personaje = Personaje.query.get(people_id)

    if not personaje:
        return jsonify({'error': 'Personaje no encontrado'}), 404
    
    favorito_existente= next((fav for fav in user.persoanjes_favoritos if fav.personaje_id == people_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El personaje ya está en favoritos'}), 400
    
    nuevo_favorito = PersonajeFavorito(usuario_id=user.id, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Personaje añadido a favoritos', 'personaje': personaje.nombre}), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
