from .database import db
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class PlanetaFavorito(db.Model):
    __tablename__ = "planetas_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id,
            "fecha_agregado": self.fecha_agregado
        }

    usuario = relationship("Usuario", back_populates="planetas_favoritos")
    planeta = relationship("Planeta", back_populates="favoritos")
    

class PersonajeFavorito(db.Model):
    __tablename__ = "personajes_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personajes.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.planeta_id,
            "fecha_agregado": self.fecha_agregado
        }

    usuario = relationship("Usuario", back_populates="personajes_favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")


class VehiculoFavorito(db.Model):
    __tablename__ = "vehiculos_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "vehiculo_id": self.planeta_id,
            "fecha_agregado": self.fecha_agregado
        }
    
    usuario = relationship("Usuario", back_populates="vehiculos_favoritos")
    vehiculo = relationship("Vehiculo", back_populates="favoritos")