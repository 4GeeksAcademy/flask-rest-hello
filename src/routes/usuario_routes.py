from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.database import db

usuario_bp = Blueprint('usuario', __name__, url_prefix='/users')


@usuario_bp.route('/', methods=['GET'])
def get_users():
    response = Usuario.query.all()
    return jsonify(response), 200


@usuario_bp.route('/favorites', methods=['GET'])
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
