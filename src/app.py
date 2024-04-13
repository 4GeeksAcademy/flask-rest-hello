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
from models import db, User, Planets, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    user_json = [{'id':user.id, 'email':user.email} for user in users]

    return jsonify(user_json), 200

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_json = [{'id':character.id, 'name':character.name, 'age':character.age, 'weight':character.weight} for character in characters]
    return jsonify(characters_json), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Characters.query.get(people_id)
    if character is None:
        return jsonify({'error': 'character not found'}), 404 

    character_json = {'id': character.id, 'name': character.name, 'age': character.age, 'weight': character.weight}
    return jsonify(character_json)

@app.route('/people', methods=['POST'])
def add_character():
    data = request.get_json()
    if 'name' not in data or 'age' not in data or 'weight' not in data:
        return jsonify({'error': 'all fields are required'}), 400

    new_character = Characters(name=data['name'], age=data['age'], weight=data['weight'])

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'message': 'Character added'}), 201 

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets_json = [{'id':planet.id, 'name':planet.name, 'population':planet.population} for planet in planets]
    return jsonify(planets_json), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id) 
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404 

    planet_json = {'id': planet.id, 'planet_name': planet.name, 'population': planet.population}
    return jsonify(planet_json)

@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    if 'name' not in data or 'population' not in data:
        return jsonify({'error': 'name and population required'}), 400

    new_planet = Planets(name=data['name'], population=data['population'])

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'message': 'Planet added'}), 201 

@app.route('/planets', methods=['DELETE'])
def delete_planet():
    try:
        # Eliminar todos los registros de la tabla Planets
        db.session.query(Planets).delete()
        db.session.commit()
        return jsonify({'message': 'Todos los registros de la tabla Planets han sido eliminados correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
