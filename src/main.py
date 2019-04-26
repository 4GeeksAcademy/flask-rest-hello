"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from models import db, Person

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(APP, db)
db.init_app(APP)


@APP.route('/')
def hello_world():
    """
    Read documentation
    """
    return jsonify(swagger(APP))


@APP.route('/person', methods=['POST', 'GET'])
def handle_person():
    """
    Create person and retrieve all persons
    """
    if request.method == 'POST':
        user1 = Person(username=request.data['username'], email='hello@gmail.com')
        db.session.add(user1)
        db.session.commit()

    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.to_json(), all_people))
        return jsonify(all_people)

    return "Invalid Method", 404


@APP.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        return user1.to_json()
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return user1.to_json()

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    APP.run(host='0.0.0.0', port=PORT)
