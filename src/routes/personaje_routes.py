from flask import Blueprint, jsonify, request
from models.personaje import Personaje
from models.database import db
from app import validar_tipo

personaje_bp = Blueprint('personajes', __name__, url_prefix='/people')

# GET people list


@personaje_bp.route('/', methods=['GET'])
def get_people():
    people = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in people]), 200

# GET person


@personaje_bp.route('/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)
    return jsonify(personaje.serialize()), 200

# DELETE person


@personaje_bp.route('/<int:people_id>', methods=['DELETE'])
def delete_personaje(people_id):
    personaje = Personaje.query.get_or_404(people_id)

    db.session.delete(personaje)
    db.session.commit()
    return jsonify({"msg": f"Personaje {people_id} eliminado"}), 200

# POST person


@personaje_bp.route('/', methods=['POST'])
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

# PUT person


@personaje_bp.route('/people/<int:people_id>', methods=['PUT'])
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
