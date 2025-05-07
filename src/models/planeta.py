from .database import db
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .associations import PlanetaFavorito

if TYPE_CHECKING:
    from .personaje import Personaje


class Planeta(db.Model):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    diametro: Mapped[int] = mapped_column(Integer, nullable=True)
    clima: Mapped[str] = mapped_column(String(50), nullable=True)
    poblacion: Mapped[int] = mapped_column(Integer, nullable=True)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)

    personajes: Mapped["Personaje"] = relationship(
        "Personaje", back_populates="planeta_natal")
    favoritos: Mapped["PlanetaFavorito"] = relationship(
        "PlanetaFavorito", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "clima": self.clima,
            "poblacion": self.poblacion,
            "imagen_url": self.imagen_url,
            "descripcion": self.descripcion
        }

    def serialize_with_relations(self):
        data = self.serialize()
        data['personajes'] = [p.serialize() for p in self.personajes]
        data['favoritos'] = [f.serialize() for f in self.favoritos]
        return data
