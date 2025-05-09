from .database import db
from sqlalchemy import String, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import VehiculoFavorito
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personaje import Personaje


class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    modelo: Mapped[str] = mapped_column(String(100), nullable=True)
    longitud: Mapped[float] = mapped_column(Float, nullable=True)
    velocidad_maxima: Mapped[int] = mapped_column(Integer, nullable=True)
    tripulacion: Mapped[int] = mapped_column(Integer, nullable=True)
    pasajeros: Mapped[int] = mapped_column(Integer, nullable=True)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    personaje_id: Mapped[int] = mapped_column(
        ForeignKey("personajes.id"), nullable=True)

    personaje: Mapped["Personaje"] = relationship(
        "Personaje",
        back_populates="vehiculo",
        uselist=False,
        foreign_keys="Personaje.vehiculo_id",
        remote_side="Personaje.vehiculo_id",
        primaryjoin="Vehiculo.id == Personaje.vehiculo_id"
    )
    favoritos: Mapped["VehiculoFavorito"] = relationship(
        "VehiculoFavorito", back_populates="vehiculo")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "longitud": self.longitud,
            "velocidad_maxima": self.velocidad_maxima,
            "tripulacion": self.tripulacion,
            "pasajeros": self.pasajeros,
            "imagen_url": self.imagen_url,
            "descripcion": self.descripcion,
            "personaje_id": self.personaje_id
        }

    def serialize_with_relations(self):
        data = self.serialize()
        if self.personaje:
            data['personaje'] = self.personaje.serialize()
        data['favoritos'] = [f.serialize() for f in self.favoritos]
        return data
