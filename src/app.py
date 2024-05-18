import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, FavoritePlanet, FavoritePerson

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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    persons = db.session.execute(db.select(User).order_by(User.id))
    person_list = [item for t in persons.all() for item in t]

    response_body = {
        'result': [i.serialize() for i in person_list]
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():

    persons = db.session.execute(db.select(Person).order_by(Person.created))
    person_list = [item for t in persons.all() for item in t]

    response_body = {
        'result': [i.serialize() for i in person_list]
    }

    return jsonify(response_body), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):

    item = db.session.execute(db.select(Person).filter_by(id=id))

    response_body = {
        'result': item.first()[0].serialize_single()
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = db.session.execute(db.select(Planet).order_by(Planet.created))
    planets_list = [item for t in planets.all() for item in t]

    response_body = {
        'result': [i.serialize() for i in planets_list]
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):

    item = db.session.execute(db.select(Planet).filter_by(id=id))

    response_body = {
        'result': item.first()[0].serialize_single()
    }

    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    user_id = request.headers.get('user')

    planets = db.session.execute(db.select(FavoritePlanet).filter_by(user_id=user_id).order_by(FavoritePlanet.id))
    planets_list = [item for t in planets.all() for item in t]

    people = db.session.execute(db.select(FavoritePerson).filter_by(user_id=user_id).order_by(FavoritePerson.id))
    people_list = [item for t in people.all() for item in t]

    response_body = {
        'result': {
            'planets': [i.serialize() for i in planets_list],
            'people': [i.serialize() for i in people_list],
        }
    }

    return jsonify(response_body), 200

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.headers.get('user')

    favoritePlanet = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(favoritePlanet)
    db.session.commit()

    response_body = {
        'result': 'Successfully added'
    }

    return jsonify(response_body), 201

@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.headers.get('user')

    favoritePerson = FavoritePerson(user_id=user_id, person_id=person_id)
    db.session.add(favoritePerson)
    db.session.commit()

    response_body = {
        'result': 'Successfully added'
    }

    return jsonify(response_body), 201

@app.route('/favorite/people/<int:favorite_person_id>', methods=['DELETE'])
def delete_favorite_person(favorite_person_id):

    item = db.session.execute(db.select(FavoritePerson).filter_by(id=favorite_person_id)).first()[0]
    db.session.delete(item)
    db.session.commit()

    return jsonify([]), 204

@app.route('/favorite/planets/<int:favorite_planet_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_planet_id):

    item = db.session.execute(db.select(FavoritePlanet).filter_by(id=favorite_planet_id)).first()[0]
    db.session.delete(item)
    db.session.commit()

    return jsonify([]), 204


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)