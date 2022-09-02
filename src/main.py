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
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/users', methods=['GET'])
def get_users():
    queryset= User.query.all()
    users_list = [user.serialize() for user in queryset]
    response_body = {
        "user_list": users_list
    }
    return jsonify(users_list), 200

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():
    #user_list = User.query.all()
    #user_list = list(map(lambda user: user.serialize(), user_list))
    # otra forma de hacerlo es esta:
    response_body = {
        # aqui pones lo que quieres que devuelva en el return
       # "msg": "Hello, this is your GET /user response ",
        "user_favorites": "hello user favoritos"
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    response_body = {"msg":"Hola people"}
    return jsonify(response_body), 200
        

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    response_body = {"id de single": people_id}
    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    response_body = {"msg":"Hola planet"}
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    response_body = {"id de planet": planet_id}
    return jsonify(response_body), 200

@app.route('/favorite', methods=['GET'])
def get_favorite():
    response_body = {"msg":"Hola favorite"}
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    response_body = {"msg":"Hola desde favorito people post"}
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    response_body = {"msg":"Hola desde favorito planet post"}
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    response_body = {"msg":"Hola desde favorito people delete"}
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    response_body = {"msg":"Hola desde favorito planet delete"}
    return jsonify(response_body), 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
