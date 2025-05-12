from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.database import db

usuario_bp = Blueprint('usuario', __name__, url_prefix='/users')

@usuario_bp.route('/', methods=['GET'])
def get_users():
    response = Usuario.query.all()
    return jsonify([u.serialize() for u in response]), 200

@usuario_bp.route('/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):

    user = Usuario.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    planetas_fav = [fav.planeta.serialize() for fav in user.planetas_favoritos] if user.planetas_favoritos else []
    personajes_fav = [fav.personaje.serialize() for fav in user.personajes_favoritos] if user.personajes_favoritos else []
    vehiculos_fav = [fav.vehiculo.serialize() for fav in user.vehiculos_favoritos] if user.vehiculos_favoritos else []

    favorites = {
        "planetas": planetas_fav,
        "personajes": personajes_fav,
        "vehiculos": vehiculos_fav
    }

    if not any(favorites.values()):
        return jsonify({"msg": "El usuario no tiene favoritos aún."}), 200

    return jsonify(favorites), 200

@usuario_bp.route('/',methods=['POST'])
def post_user():
    user_list = Usuario.query.all()
    user_id = len(user_list)+1

    request_body = request.get_json()

    if not request_body:
        return jsonify({"error": "Empty request body"}), 400
    # Validate required fields and their types
    if not isinstance(request_body.get("nombre"), str):
        return jsonify({"error": "'nombre' must be a string"}), 400
    if not isinstance(request_body.get("apellido"), str):
        return jsonify({"error": "'apellido' must be a string"}), 400
    if not isinstance(request_body.get("email"), (str)):
        return jsonify({"error": "'email' must be a string"}), 400
    if not isinstance(request_body.get("password"), (str)):
        return jsonify({"error": "'password' must be a string"}), 400
    
    new_user = Usuario(
        nombre=request_body['nombre'],
        apellido=request_body['apellido'],
        email=request_body['email'],
        password=request_body['password'],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201