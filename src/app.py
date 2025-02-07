import os
from enum import Enum
import bcrypt

from utils import APIException, generate_sitemap
from admin import setup_admin

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import or_
from models import Characters, FavouriteType, Favourites, Planets, Starships, Users, db
from flask_jwt_extended import create_access_token, get_csrf_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#JWT
app.config["JWT_SECRET_KEY"] = ("super-secret")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_COOKIE_SECURE"] = True 

jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, supports_credentials=True)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

tables = {
    "starships": Starships,
    "characters": Characters,
    "planets": Planets
}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    required_fields = ["user_name", "email", "password"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = db.session.query(Users).filter(or_(Users.user_name == user_name, Users.email == email)).first()
    if existing_user:
        return jsonify({"error": "Username or Email already registered"}), 400

    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = Users(user_name=user_name, email=email, password=hashedPassword)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def get_login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    required_fields = ["email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 400

    is_password_valid = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

    if not is_password_valid:
        return jsonify({"error": "Password not correct"}), 400
    
    access_token = create_access_token(identity=str(user.id))
    csrf_token = get_csrf_token(access_token)
    response = jsonify({
        "msg": "login successful",
        "user": user,
        "csrf_token": csrf_token
        })
    set_access_cookies(response, access_token)
    
    return response


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/characters", methods=["GET"])
def get_characters():
    characters = Characters.query.all()
    return jsonify(characters), 200

@app.route("/characters/<int:people_id>", methods=["GET"])
def get_character(people_id):
    result = (
        db.session.query(Characters, Planets)
        .join(Planets, Characters.home_world == Planets.id)
        .filter(Characters.id == people_id)
        .first()
    )
    character, home_world = result
    character.home_world = home_world
    return jsonify(character) if character else (jsonify({"error": "Character not found"}), 404)

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    return jsonify(planets), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify(planet) if planet else (jsonify({"error": "Planet not found"}), 404)

@app.route("/starships", methods=["GET"])
def get_starships():
    starships = Starships.query.all()
    return jsonify(starships), 200

@app.route("/starships/<int:starship_id>", methods=["GET"])
def get_starship(starship_id):
    starship = Starships.query.get(starship_id)
    return jsonify(starship) if starship else (jsonify({"error": "Starship not found"}), 404)

@app.route("/favourites/", methods=["GET", "POST", "DELETE"])
@jwt_required()
def handle_favourites():
    user_id = get_jwt_identity()
    if request.method == "GET":
        favorites = Favourites.query.filter_by(user_id=user_id).all()
        return jsonify(favorites), 200

    data = request.get_json()

    if request.method == "POST":
        required_fields = ["type", "external_id", "name"]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        if not (data["type"] in FavouriteType.__members__):
            return jsonify({"error": "Type not valid"}), 400
        if Favourites.query.filter_by(external_id=data["external_id"], user_id=user_id, type=data["type"]).first():
            return jsonify({"error": "Resource already favourited"}), 400
        if not tables[data["type"]].query.filter_by(id=data["external_id"]).first():
            return jsonify({"error": "Resource not found"}), 400

        new_fav = Favourites(
            external_id=data["external_id"],
            type=data["type"],
            name=data["name"],
            user_id=user_id,
        )
        db.session.add(new_fav)
        db.session.commit()

        return jsonify(new_fav), 201

    if request.method == "DELETE":
        required_fields = ["id"]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        favorite = Favourites.query.filter_by(
            id=data["id"], user_id=user_id
        ).first()

        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Favorite deleted successfully"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=PORT, debug=False)
