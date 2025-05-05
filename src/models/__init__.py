from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Float, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

from .usuario import Usuario
from .personaje import Personaje
from .vehiculo import Vehiculo
from .planeta import Planeta
from .associations import PersonajeFavorito, PlanetaFavorito, VehiculoFavorito