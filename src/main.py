"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People
from models import Planet
from models import Favorites

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


# GET
@app.route('/user', methods=['GET'])
def get_user():
    queryset= User.query.all()
    user_list = [user.serialize() for user in queryset]
    response_body = {

        "success": True,
        "results": user_list,
        "msg": "hola"
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites_list = Favorites.query.all()
    favorites_list = list(map(lambda favorites: favorites.serialize(), favorites_list))
    response_body = {
        "success": True,
        "results": favorites_list,
        "msg": "hola desde favorites"
        }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_list = list(map(lambda people: people.serialize(), people))
    response_body = {
        "success": True,
        "results": people_list,
        "msg": "hola desde people"
        }
    return jsonify(response_body), 200



@app.route('/planet', methods=['GET'])
def get_planet():
    planet_list = Planet.query.all()
    planet_list = list(map(lambda planet: planet.serialize(), planet_list))
    response_body = {
        "success": True,
        "results": planet_list,
        "msg": "hola desde planet"
        }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    people = People.query.get(people_id)
    response_body = {
        "success": True,
        "results": people,
        "msg": "hola desde people"
        }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    response_body = {
        "success": True,
        "results": planet,
        "msg": "hola desde planet"
        }
    return jsonify(response_body), 200




# POST

@app.route('/people', methods=['POST'])
def post_people():
    body = json.loads(request.data)
    new_people = People(
        name = body["name"],
        gender = body["gender"],
        birthday_year = body["birthday_year"],
        color_eyes = body["color_eyes"],
        height = body["height"],
        mass = body["mass"]
    )
    db.session.add(new_people)
    db.session.commit()
    response_body = {  
        "success": True,
        "results": new_people,
        "resultado": "añadido personaje"
    }
    return jsonify(response_body), 200   


""" @app.route('/people/<int:people_id>', methods=['POST'])
def post_single_people(people_id):
    body = json.loads(request.data)
    new_single_people = People(
            name  = "name",
            gender = "gender",
            birthday_year = "birthday_year",
            color_eyes  = "color_eyes",
            height = "height",
            mass = "mass")
    db.session.add(new_single_people)
    db.session.commit()
    response_body = {  
        "success": True,
        "results": new_single_people,
        "resultado": "añadido personaje"
    }
    return jsonify(response_body), 200 """


# DELETE 

""" @app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    response_body = {"msg":"Hola desde people delete"}
    return jsonify(response_body), 200
 """






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
