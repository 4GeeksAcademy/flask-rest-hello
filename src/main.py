import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from models import db, Person

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def hello_world():
    """
    Read documentation
    """
    return jsonify(swagger(app))


@app.route('/person', methods=['POST', 'GET'])
def handle_person():
    if request.method == 'POST':
        """return the information for <user_id>"""
        user1 = Person(username=request.data['username'], email='hello@gmail.com')
        db.session.add(user1)
        db.session.commit()

    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.to_json(), all_people))
        return jsonify(all_people)

    return "Invalid Method", 404


@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        return user1.to_json()
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return user1.to_json()

    return "Invalid Method", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)