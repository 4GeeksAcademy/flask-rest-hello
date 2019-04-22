from flask import Flask
from flask import jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alex:12341234@localhost/hellodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username
        
    def to_json(self):
        return jsonify({
            "username": self.username,
            "email": self.email
        })
        
        
@app.route('/')
def hello_world():
    user1 = Person(username='alesanchezr', email='hello@gmail.com')
    db.session.add(user1)
    db.session.commit()
    return 'Hello, World!'
        
@app.route('/person/<int:person_id>')
def get_single_person(person_id):
    user1 = Person.query.get(person_id)
    return user1.to_json()
    
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))