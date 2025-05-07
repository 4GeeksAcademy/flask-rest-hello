from .database import db
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .vehiculo import Vehiculo


class Personaje(db.Model):
    __tablename__ = "personajes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    especie: Mapped[str] = mapped_column(String(50), nullable=True)
    altura: Mapped[int] = mapped_column(Integer, nullable=True)
    peso: Mapped[int] = mapped_column(Integer, nullable=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    planeta_natal_id: Mapped[int] = mapped_column(
        ForeignKey("planetas.id"), nullable=True)
    vehiculo_id: Mapped[int] = mapped_column(
        ForeignKey("vehiculos.id"), unique=True, nullable=True)

    vehiculo = relationship(
        "Vehiculo",
        back_populates="personaje",
        uselist=False,
        # foreign_keys=[Vehiculo.personaje_id]
    )
    planeta_natal = relationship("Planeta", back_populates="personajes")
    favoritos = relationship("PersonajeFavorito", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "altura": self.altura,
            "peso": self.peso,
            "genero": self.genero,
            "imagen_url": self.imagen_url,
            "descripcion": self.descripcion
        }

    def serialize_with_relations(self):
        data = self.serialize()
        if self.planeta_natal:
            data['planeta_natal'] = self.planeta_natal.serialize()
        if self.vehiculo:
            data['vehiculo'] = self.vehiculo.serialize()
        data['favoritos'] = [f.serialize() for f in self.favoritos]
        return data
