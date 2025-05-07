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
from models import db, Personaje, Planeta, Vehiculo, Usuario, PersonajeFavorito, PlanetaFavorito, VehiculoFavorito


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

with app.app_context():
    print("Tablas registradas:", db.metadata.tables.keys())
    db.create_all()

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

@app.route('/users/favorites', methods=['GET'])
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
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = PlanetaFavorito.query.filter_by(usuario_id=user_id, planeta_id=planet_id).first()

    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = PlanetaFavorito.query.filter_by(usuario_id=user_id).all()
    return jsonify([fav.serialize() for fav in updated_favorites]), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
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
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
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

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
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

    new_personaje = Personaje(
        nombre=request_body['nombre'],
        especie=request_body['especie'],
        altura=request_body['altura'],
        peso=request_body['peso'],
        genero=request_body['genero'],
        imagen_url=request_body['imagen_url'],
        descripcion=request_body['descripcion']
    )

    db.session.add(new_personaje)
    db.session.commit()

    return jsonify({"message": "Personaje created successfully"}), 201


### PUTs

def validar_tipo(valor, tipo_esperado, nombre_campo):
    if valor is not None and not isinstance(valor, tipo_esperado):
        raise ValueError(f"Campo '{nombre_campo}' debe ser de tipo {tipo_esperado.__name__}")

# PUT Personajes
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)
    data = request.get_json()

    try:
        if "nombre" in data:
            validar_tipo(data["nombre"], str, "nombre")
            personaje.nombre = data["nombre"]
        if "especie" in data:
            validar_tipo(data["especie"], str, "especie")
            personaje.especie = data["especie"]
        if "altura" in data:
            validar_tipo(data["altura"], int, "altura")
            personaje.altura = data["altura"]
        if "peso" in data:
            validar_tipo(data["peso"], int, "peso")
            personaje.peso = data["peso"]
        if "genero" in data:
            validar_tipo(data["genero"], str, "genero")
            personaje.genero = data["genero"]
        if "descripcion" in data:
            validar_tipo(data["descripcion"], str, "descripcion")
            personaje.descripcion = data["descripcion"]
        if "planeta_natal_id" in data:
            validar_tipo(data["planeta_natal_id"], int, "planeta_natal_id")
            personaje.planeta_natal_id = data["planeta_natal_id"]
        if "vehiculo_id" in data:
            validar_tipo(data["vehiculo_id"], int, "vehiculo_id")
            personaje.vehiculo_id = data["vehiculo_id"]

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    db.session.commit()
    return jsonify(personaje.serialize()), 200

# PUT Planetas
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)
    data = request.get_json()

    try:
        if "nombre" in data:
            validar_tipo(data["nombre"], str, "nombre")
            planeta.nombre = data["nombre"]
        if "diametro" in data:
            validar_tipo(data["diametro"], int, "diametro")
            planeta.diametro = data["diametro"]
        if "clima" in data:
            validar_tipo(data["clima"], str, "clima")
            planeta.clima = data["clima"]
        if "poblacion" in data:
            validar_tipo(data["poblacion"], int, "poblacion")
            planeta.poblacion = data["poblacion"]
        if "descripcion" in data:
            validar_tipo(data["descripcion"], str, "descripcion")
            planeta.descripcion = data["descripcion"]

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    db.session.commit()
    return jsonify(planeta.serialize()), 200

# PUT Vehiculos
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehiculo(vehicle_id):
    vehiculo = Vehiculo.query.get_or_404(vehicle_id)
    data = request.get_json()

    try:
        if "nombre" in data:
            validar_tipo(data["nombre"], str, "nombre")
            vehiculo.nombre = data["nombre"]
        if "modelo" in data:
            validar_tipo(data["modelo"], str, "modelo")
            vehiculo.modelo = data["modelo"]
        if "longitud" in data:
            validar_tipo(data["longitud"], float, "longitud")
            vehiculo.longitud = data["longitud"]
        if "velocidad_maxima" in data:
            validar_tipo(data["velocidad_maxima"], int, "velocidad_maxima")
            vehiculo.velocidad_maxima = data["velocidad_maxima"]
        if "tripulacion" in data:
            validar_tipo(data["tripulacion"], int, "tripulacion")
            vehiculo.tripulacion = data["tripulacion"]
        if "pasajeros" in data:
            validar_tipo(data["pasajeros"], int, "pasajeros")
            vehiculo.pasajeros = data["pasajeros"]
        if "descripcion" in data:
            validar_tipo(data["descripcion"], str, "descripcion")
            vehiculo.descripcion = data["descripcion"]
        if "personaje_id" in data:
            validar_tipo(data["personaje_id"], int, "personaje_id")
            vehiculo.personaje_id = data["personaje_id"]

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    db.session.commit()
    return jsonify(vehiculo.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
