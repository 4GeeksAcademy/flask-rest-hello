from flask import Blueprint, jsonify, request
from models import db, Personaje, Planeta, Vehiculo, Usuario, PersonajeFavorito, PlanetaFavorito, VehiculoFavorito
from models.database import db
from app import validar_tipo

favoritos_bp = Blueprint('favoritos', __name__, url_prefix='/favorite')


@favoritos_bp.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = PlanetaFavorito.query.filter_by(
        usuario_id=user_id, planeta_id=planet_id).first()

    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = PlanetaFavorito.query.filter_by(
        usuario_id=user_id).all()
    return jsonify([fav.serialize() for fav in updated_favorites]), 200


@favoritos_bp.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_person(people_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = PersonajeFavorito.query.filter_by(
        usuario_id=user_id, personaje_id=people_id).first()

    if not favorite:
        return jsonify({"message": "Person not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = PersonajeFavorito.query.filter_by(
        usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_favorites]), 200


@favoritos_bp.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehiculo(vehicle_id):
    user_id = Usuario.query.get(Usuario.id)
    favorite = VehiculoFavorito.query.filter_by(
        usuario_id=user_id, vehiculo_id=vehicle_id).first()

    if not favorite:
        return jsonify({"message": "Vehículo favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    updated_favorites = VehiculoFavorito.query.filter_by(
        usuario_id=user_id).all()
    return jsonify([p.serialize() for p in updated_favorites]), 200


@favoritos_bp.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = Usuario.query.get(Usuario.id)
    planeta = Planeta.query.get(planet_id)

    if not planeta:
        return jsonify({'error': 'Planeta no encontrado'}), 404

    favorito_existente = next(
        (fav for fav in user.planetas_favoritos if fav.planeta_id == planet_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El planeta ya está en favoritos'}), 400
    nuevo_favorito = PlanetaFavorito(usuario_id=user.id, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Planeta añadido a favoritos', 'planeta': planeta.nombre}), 201


@favoritos_bp.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_personaje(people_id):
    user = Usuario.query.get(Usuario.id)
    personaje = Personaje.query.get(people_id)

    if not personaje:
        return jsonify({'error': 'Personaje no encontrado'}), 404

    favorito_existente = next(
        (fav for fav in user.persoanjes_favoritos if fav.personaje_id == people_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El personaje ya está en favoritos'}), 400

    nuevo_favorito = PersonajeFavorito(
        usuario_id=user.id, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Personaje añadido a favoritos', 'personaje': personaje.nombre}), 201


@favoritos_bp.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehiculo(vehicle_id):
    user = Usuario.query.get(Usuario.id)
    vehiculo = Vehiculo.query.get(vehicle_id)

    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

    favorito_existente = next(
        (fav for fav in user.vehiculos_favoritos if fav.vehiculo_id == vehicle_id), None)
    if favorito_existente:
        return jsonify({'msg': 'El vehículo ya está en favoritos'}), 400

    nuevo_favorito = VehiculoFavorito(
        usuario_id=user.id, vehiculo_id=vehicle_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({'msg': 'Vehículo añadido a favoritos', 'vehiculo': vehiculo.nombre}), 201
