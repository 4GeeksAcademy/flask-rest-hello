"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from http import HTTPStatus
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Personaje, Planeta, Vehiculo, db, User

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


##############################################################################################################


@app.route("/users", methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([user.serialize() for user in users]), HTTPStatus.OK


@app.route("/users/<int:user_id>", methods=['GET'])
def get_user_by_id(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"msg": "user not found"}), 404

    return jsonify(user.serialize()), HTTPStatus.OK


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get("user_id", type=int)
    current_user = db.session.get(User, user_id)
    if not current_user:
        return jsonify({"msg": "user not found"}), 404
    return jsonify({
        'personajes': [personaje.serialize() for personaje in current_user.personajes_favoritos],
        'planetas': [planeta.serialize() for planeta in current_user.planetas_favoritos]
    }), HTTPStatus.OK


##############################################################################################################


@app.route('/personajes', methods=['GET'])
def get_personajes():
    try:
        personajes = db.session.execute(db.select(Personaje)).scalars().all()
        return jsonify([personaje.serialize() for personaje in personajes]), HTTPStatus.OK
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_single_person(personaje_id: int):
    try:
        personaje = db.session.get(Personaje, personaje_id)
        if personaje is None:
            raise APIException("Personaje no encontrado",
                               status_code=HTTPStatus.NOT_FOUND)
        return jsonify(personaje.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


##############################################################################################################


@app.route('/planetas', methods=['GET'])
def get_planetas():
    try:
        planetas = db.session.execute(db.select(Planeta)).scalars().all()
        return jsonify([planeta.serialize() for planeta in planetas]), HTTPStatus.OK
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_single_planeta(planeta_id: int):
    try:
        planeta = db.session.get(Planeta, planeta_id)
        if planeta is None:
            raise APIException(
                "Planeta no encontrado",
                status_code=HTTPStatus.NOT_FOUND
            )
        return jsonify(planeta.serialize()), HTTPStatus.OK
    except APIException:
        raise
    except Exception as e:
        raise APIException(
            str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


##############################################################################################################


@app.route('/favorite/personajes/<int:personaje_id>', methods=['POST'])
def add_favorite_people(personaje_id):
    user_id = request.args.get("user_id", type=int)
    current_user = db.session.get(User, user_id)
    if not current_user:
        raise APIException("Usuario no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    personaje = db.session.get(Personaje, personaje_id)
    if personaje is None:
        raise APIException("Personaje no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    current_user.personajes_favoritos.append(personaje)
    db.session.commit()
    return jsonify({"msg": "Personaje marcado como favorito"}), HTTPStatus.CREATED


@app.route('/favorite/planetas/<int:planeta_id>', methods=['POST'])
def add_favorite_planet(planeta_id: int):
    user_id = request.args.get("user_id", type=int)
    current_user = db.session.get(User, user_id)
    if not current_user:
        raise APIException("Usuario no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    planeta = db.session.get(Planeta, planeta_id)
    if planeta is None:
        raise APIException("Planeta no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    current_user.planetas_favoritos.append(planeta)
    db.session.commit()
    return jsonify({"msg": "Planeta marcado como favorito"}), HTTPStatus.CREATED


##############################################################################################################



@app.route('/favorite/planetas/<int:planeta_id>', methods=['DELETE'])
def delete_favorite_planet(planeta_id: int):
    user_id = request.args.get("user_id", type=int)
    current_user = db.session.get(User, user_id)
    if not current_user:
        raise APIException("Usuario no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    planeta = db.session.get(Planeta, planeta_id)
    if planeta is None:
        raise APIException("Planeta no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    if planeta not in current_user.planetas_favoritos:
        raise APIException("Planeta no esta marcado como favorito",
                           status_code=HTTPStatus.NOT_FOUND)

    current_user.planetas_favoritos.remove(planeta)
    db.session.commit()
    return jsonify({"msg": "Planeta eliminado de los favoritos del usuario"}), HTTPStatus.OK


@app.route('/favorite/personajes/<int:personaje_id>', methods=['DELETE'])
def delete_favorite_personaje(personaje_id: int):
    user_id = request.args.get("user_id", type=int)
    current_user = db.session.get(User, user_id)
    if not current_user:
        raise APIException("Usuario no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    personaje = db.session.get(Personaje, personaje_id)
    if personaje is None:
        raise APIException("Personaje no encontrado",
                           status_code=HTTPStatus.NOT_FOUND)

    if personaje not in current_user.personajes_favoritos:
        raise APIException("Personaje no esta marcado como favorito",
                           status_code=HTTPStatus.NOT_FOUND)

    current_user.personajes_favoritos.remove(personaje)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado de los favoritos del usuario"}), HTTPStatus.OK


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
