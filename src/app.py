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
from models import db, Personaje, Planeta, Vehiculo, Usuario, PersonajeFavorito, PlanetaFavorito, VehiculoFavorito
from routes.personaje_routes import personaje_bp
from routes.planeta_routes import planeta_bp
from routes.vehiculo_routes import vehiculo_bp
from routes.usuario_routes import usuario_bp
from routes.favoritos_routes import favoritos_bp


app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

with app.app_context():
    print("Tablas registradas:", db.metadata.tables.keys())
    db.create_all()

app.register_blueprint(personaje_bp)
app.register_blueprint(planeta_bp)
app.register_blueprint(vehiculo_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(favoritos_bp)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

def validar_tipo(valor, tipo_esperado, nombre_campo):
    if valor is not None and not isinstance(valor, tipo_esperado):
        raise ValueError(
            f"Campo '{nombre_campo}' debe ser de tipo {tipo_esperado.__name__}")

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
