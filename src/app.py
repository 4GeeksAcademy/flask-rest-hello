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
from models import db, User, Planets, Characters, Favorite_planet, Favorite_character
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
    user_json = [user.serialize() for user in users]

    return jsonify(user_json), 200

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        raise APIException('all fields are required', status_code=400)

    new_user = User(
            email=data['email'], 
            password=data['password'], 
            is_active=data.get('is_active',True)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Character added'}), 201 

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Favorite character erased'})
    except Exception as e:
        db.session.rollback()
        raise APIException('error', status_code=500)
    

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    characters_json = list(map(lambda x: x.serialize(), characters ))
    return jsonify(characters_json), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Characters.query.get(people_id)
    if character is None:
        raise APIException('error: character not found', status_code=404)

    character_json = {'id': character.id, 'name': character.name, 'age': character.age, 'weight': character.weight}
    return jsonify(character_json)

@app.route('/people', methods=['POST'])
def add_character():
    data = request.get_json()
    if 'name' not in data or 'age' not in data or 'weight' not in data:
        raise APIException('all fields are required', status_code=400)

    new_character = Characters(name=data['name'], age=data['age'], weight=data['weight'])

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'message': 'Character added'}), 201 

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets_json = [planet.serialize() for planet in planets]
    return jsonify(planets_json), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id) 
    if planet is None:
        raise APIException('planet not found', status_code=404) 

    planet_json = {'id': planet.id, 'planet_name': planet.name, 'population': planet.population}
    return jsonify(planet_json)

@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
    if 'name' not in data or 'population' not in data:
        raise APIException('all fields are required', status_code=400)

    new_planet = Planets(name=data['name'], population=data['population'])

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'message': 'Planet added'}), 201 

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = Planets.query.get(planet_id)
    if 'favorite_planet' not in data or 'user_id' not in data:
        raise APIException('favorite_planet and user_id required', status_code=400)

    new_planet = Favorite_planet(name=data['favorite_planet'], user_id=data['user_id'])

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'message': 'Favorite planet added'}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character():
    data = request.get_json()
    if 'favorite_character' not in data or 'user_id' not in data:
        raise APIException('favorite_character and user_id required', status_code=400)

    new_character = Favorite_character(name=data['favorite_character'], user_id=data['user_id'])

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'message': 'Favorite character added'}), 201  

@app.route('/favorites/<int:user_id>', methods=['GET'])
def get_all_favorites(user_id):
    planets = Favorite_planet.query.all(user_id)
    characters = Favorite_character.query.all(user_id)
    planets_json = [planet.serialize() for planet in planets]
    characters_json = [character.serialize() for character in characters]
    all_favorites = {'planets': planets_json, 'characters':characters_json}
    return jsonify(all_favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        planet = Favorite_planet.query.get(planet_id)
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'Favorite planet erased'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/favorite/planet/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    try:
        character = Favorite_character.query.get(people_id)
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Favorite character erased'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        planet = Planets.query.get(planet_id)
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'Planet erased'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_character(people_id):
    try:
        character = Characters.query.get(people_id)
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Character erased'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    try:
        data = request.get_json()
        planet = Planets.query.get(planet_id)
        if planet is None:
            raise APIException('planet not found', status_code=404)

        if 'name' in data:
            planet.name = data['name']
        if 'population' in data:
            planet.population = data['population']
        db.session.commit()
        return jsonify({'message': 'Planet updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_character(people_id):
    try:
        data = request.get_json()
        character = Characters.query.get(people_id)
        if character is None:
            raise APIException('character not found', status_code=404) 

        if 'name' in data:
            character.name = data['name']
        if 'population' in data:
            character.age = data['age']
        if 'weight' in data:
            character.weight = data['weight']
        db.session.commit()
        return jsonify({'message': 'Character updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
