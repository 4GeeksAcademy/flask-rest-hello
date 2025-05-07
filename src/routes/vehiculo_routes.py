from flask import Blueprint, jsonify, request
from models.vehiculo import Vehiculo
from models.database import db
from app import validar_tipo

vehiculo_bp = Blueprint('vehiculos', __name__, url_prefix='/vehicles')


@vehiculo_bp.route('/', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([vehiculo.serialize() for vehiculo in vehiculos]), 200

@vehiculo_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehiculo(vehicle_id):
    vehiculo = Vehiculo.query.get_or_404(vehicle_id)
    return jsonify(vehiculo.serialize()), 200


@vehiculo_bp.route('/', methods=['POST'])
def post_vehiculo():
    request_body = request.get_json()

    if not request_body:
        return jsonify({"error": "Empty request body"}), 400

    # Validate required fields and their types
    if not isinstance(request_body.get("nombre"), str):
        return jsonify({"error": "'nombre' must be a string"}), 400
    if not isinstance(request_body.get("modelo"), str):
        return jsonify({"error": "'modelo' must be a string"}), 400
    if not isinstance(request_body.get("longitud"), (int, float)):
        return jsonify({"error": "'longitud' must be a number"}), 400
    if not isinstance(request_body.get("velocidad_maxima"), (int, float)):
        return jsonify({"error": "'velocidad_maxima' must be a number"}), 400
    if not isinstance(request_body.get("tripulacion"), int):
        return jsonify({"error": "'tripulacion' must be a string"}), 400
    if not isinstance(request_body.get("pasajeros"), int):
        return jsonify({"error": "'pasajeros' must be a string"}), 400
    if not isinstance(request_body.get("image_url"), str):
        return jsonify({"error": "'imagen_url' must be a string"}), 400
    if not isinstance(request_body.get("descripcion"), str):
        return jsonify({"error": "'descripcion' must be a string"}), 400

    new_vehiculo = Vehiculo(
        nombre=request_body['nombre'],
        modelo=request_body['modelo'],
        longitud=request_body['longitud'],
        velocidad_maxima=request_body['velocidad_maxima'],
        tripulacion=request_body['tripulacion'],
        pasajeros=request_body['pasajeros'],
        imagen_url=request_body['imagen_url'],
        descripcion=request_body['descripcion']
    )

    db.session.add(new_vehiculo)
    db.session.commit()

    return jsonify({"message": "Vehiculo created successfully"}), 201


@vehiculo_bp.route('/<int:vehicle_id>', methods=['PUT'])
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


@vehiculo_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehiculo(vehicle_id):
    vehiculo = Vehiculo.query.get_or_404(vehicle_id)

    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({"msg": f"Vehículo {vehicle_id} eliminado"}), 200