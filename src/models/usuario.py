from .database import db
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    ultima_conexion: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    activo: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Relaciones
    planetas_favoritos = relationship("PlanetaFavorito", back_populates="usuario")
    personajes_favoritos = relationship("PersonajeFavorito", back_populates="usuario")
    vehiculos_favoritos = relationship("VehiculoFavorito", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "fecha_registro": self.fecha_registro,
            "ultima_conexion": self.ultima_conexion,
            "activo": self.activo
        }
    
    def serialize_with_relations(self):
        data = self.serialize()
        data['planetas_favoritos'] = [pf.serialize() for pf in self.planetas_favoritos]
        data['personajes_favoritos'] = [pef.serialize() for pef in self.personajes_favoritos]
        data['vehiculos_favoritos'] = [vf.serialize() for vf in self.vehiculos_favoritos]
        return data