from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/person', methods=['POST', 'GET'])
def handle_person():
    if request.method == 'POST':
        """return the information for <user_id>"""
        user1 = Person(username='alesanchezr', email='hello@gmail.com')
        db.session.add(user1)
        db.session.commit()

    if request.method == 'GET':
        return 'Hello, World!'


@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        return user1.to_json()
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return user1.to_json()