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


app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo global de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Genera un mapa visual de todas las rutas
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS DE PERSONAJES
@app.route('/people', methods=['GET'])
def get_people():
    people = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)
    return jsonify(personaje.serialize()), 200

# ENDPOINTS DE PLANETAS
@app.route('/planets', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)
    return jsonify(planeta.serialize()), 200

# ENDPOINTS DE VEHICULOS
@app.route('/vehicles', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([vehiculo.serialize() for vehiculo in vehiculos]), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehiculo(vehicle_id):
    vehiculo = Vehiculo.query.get_or_404(vehicle_id)
    return jsonify(vehiculo.serialize()), 200

# ENDPOINTS DE USUARIOS Y FAVORITOS
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

# ENDPOINTS DE FAVORITOS - ELIMINAR
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
    favorite = PersonajeFavorito.query.filter_by(usuario_id=user_id, personaje_id=people_id).first()

    if not favorite:
        return jsonify({"message": "Person not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = PersonajeFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_favorites]), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehiculo(vehicle_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = VehiculoFavorito.query.filter_by(usuario_id=user_id, vehiculo_id=vehicle_id).first()

    if not favorite:
        return jsonify({"message": "Vehículo favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = VehiculoFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_favorites]), 200

# ENDPOINTS DE ELIMINAR
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)

    db.session.delete(planeta)
    db.session.commit()
    return jsonify({"msg": f"Planeta {planet_id} eliminado"}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)

    db.session.delete(personaje)
    db.session.commit()
    return jsonify({"msg": f"Personaje {people_id} eliminado"}), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehiculo(vehicle_id):
    vehiculo = Vehiculo.query.get_or_404(vehicle_id)

    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({"msg": f"Vehículo {vehicle_id} eliminado"}), 200

# ENDPOINTS DE FAVORITOS - AÑADIR
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

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehiculo(vehicle_id):
    user = Usuario.query.get(Usuario.id)
    vehiculo = Vehiculo.query.get(vehicle_id)

    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

    favorito_existente = next((fav for fav in user.vehiculos_favoritos if fav.vehiculo_id == vehicle_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El vehículo ya está en favoritos'}), 400

    nuevo_favorito = VehiculoFavorito(usuario_id=user.id, vehiculo_id=vehicle_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Vehículo añadido a favoritos','vehiculo': vehiculo.nombre}), 201

### POSTs

#POST Personajes
@app.route('/people', methods=['POST'])
def post_people():
    request_body = request.get_json()

    if not request_body:
        return jsonify({"error": "Empty request body"}), 400

    # Validate required fields and their types
    if not isinstance(request_body.get("nombre"), str):
        return jsonify({"error": "'nombre' must be a string"}), 400
    if not isinstance(request_body.get("especie"), str):
        return jsonify({"error": "'especie' must be a string"}), 400
    if not isinstance(request_body.get("altura"), (int, float)):
        return jsonify({"error": "'altura' must be a number"}), 400
    if not isinstance(request_body.get("peso"), (int, float)):
        return jsonify({"error": "'peso' must be a number"}), 400
    if not isinstance(request_body.get("genero"), str):
        return jsonify({"error": "'genero' must be a string"}), 400
    if not isinstance(request_body.get("imagen_url"), str):
        return jsonify({"error": "'imagen_url' must be a string"}), 400
    if not isinstance(request_body.get("descripcion"), str):
        return jsonify({"error": "'descripcion' must be a string"}), 400

    # At this point, request_body is validated
    # You can now create and save a new Personaje object, for example

    return jsonify({"message": "Personaje created successfully"}), 201


### PUTs
# PUT Personajes
@app.route('/people/<int:people_id>', methods=['PUT'])
def put_people(people_id):
    data = Personaje.query.get_or_404(people_id)
    request_body = request.get_json()

    if not request_body:
        return jsonify({"error": "Empty request body"}), 400

    # Validate required fields and their types
    if not isinstance(request_body.get("nombre"), str):
        return jsonify({"error": "'nombre' must be a string"}), 400
    else:
        data.nombre = request_body.nombre
    if not isinstance(request_body.get("especie"), str):
        return jsonify({"error": "'especie' must be a string"}), 400
    else:
        data.especie = request_body.especie
    if not isinstance(request_body.get("altura"), (int, float)):
        return jsonify({"error": "'altura' must be a number"}), 400
    else:
        data.altura = request_body.altura
    if not isinstance(request_body.get("peso"), (int, float)):
        return jsonify({"error": "'peso' must be a number"}), 400
    else:
        data.peso = request_body.peso
    if not isinstance(request_body.get("genero"), str):
        return jsonify({"error": "'genero' must be a string"}), 400
    else:
        data.genero = request_body.genero
    if not isinstance(request_body.get("imagen_url"), str):
        return jsonify({"error": "'imagen_url' must be a string"}), 400
    else:
        data.image_url = request_body.image_url
    if not isinstance(request_body.get("descripcion"), str):
        return jsonify({"error": "'descripcion' must be a string"}), 400
    else:
        data.descripcion = request_body.descripcion

    # At this point, request_body is validated
    # You can now create and save a new Personaje object, for example

    return jsonify({"message": "Personaje updated successfully"}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
