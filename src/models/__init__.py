from .favoritos import PersonajeFavorito, VehiculoFavorito, PlanetaFavorito
from .usuario import Usuario
from .planeta import Planeta
from .vehiculo import Vehiculo
from .personaje import Personaje
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
