from flask import Blueprint, jsonify, request
from models.planeta import Planeta
from models.database import db


planeta_bp = Blueprint('planetas', __name__, url_prefix='/planets')


@planeta_bp.route('/', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200


@planeta_bp.route('/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)
    return jsonify(planeta.serialize()), 200


@planeta_bp.route('/<int:planet_id>', methods=['DELETE'])
def delete_planeta(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)

    db.session.delete(planeta)
    db.session.commit()
    return jsonify({"msg": f"Planeta {planet_id} eliminado"}), 200


@planeta_bp.route('/', methods=['POST'])
def post_planeta():
    request_body = request.get_json()
    if not request_body:
        return jsonify({"error": "Empty request body"}), 400

    # Validate required fields and their types
    if not isinstance(request_body.get("nombre"), str):
        return jsonify({"error": "'nombre' must be a string"}), 400
    if not isinstance(request_body.get("diametro"), int):
        return jsonify({"error": "'diametro' must be a string"}), 400
    if not isinstance(request_body.get("clima"), str):
        return jsonify({"error": "'clima' must be a number"}), 400
    if not isinstance(request_body.get("poblacion"), int):
        return jsonify({"error": "'poblacion' must be a number"}), 400
    if not isinstance(request_body.get("imagen_url"), str):
        return jsonify({"error": "'imagen_url' must be a string"}), 400
    if not isinstance(request_body.get("descripcion"), str):
        return jsonify({"error": "'descripcion' must be a string"}), 400

    new_planeta = Planeta(
        nombre=request_body['nombre'],
        diametro=request_body['diametro'],
        clima=request_body['clima'],
        poblacion=request_body['poblacion'],
        imagen_url=request_body['imagen_url'],
        descripcion=request_body['descripcion']
    )

    db.session.add(new_planeta)
    db.session.commit()

    return jsonify({"message": "Planet created successfully"}), 201

def validar_tipo(valor, tipo_esperado, nombre_campo):
    if valor is not None and not isinstance(valor, tipo_esperado):
        raise ValueError(
            f"Campo '{nombre_campo}' debe ser de tipo {tipo_esperado.__name__}")

@planeta_bp.route('/<int:planet_id>', methods=['PUT'])
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
