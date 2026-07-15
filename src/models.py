from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


personajes_favoritos_tabla = db.Table(
    "personajes_favoritos",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("personaje_id", ForeignKey("personaje.id"), primary_key=True),
)

vehiculos_favoritos_tabla = db.Table(
    "vehiculos_favoritos",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("vehiculo_id", ForeignKey("vehiculo.id"), primary_key=True),
)

planetas_favoritos_tabla = db.Table(
    "planetas_favoritos",
    db.Column("user_id", ForeignKey("user.id"), primary_key=True),
    db.Column("planeta_id", ForeignKey("planeta.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    personajes_favoritos: Mapped[list["Personaje"]] = relationship(
        secondary=personajes_favoritos_tabla,
        back_populates="favorited_by"
    )
    vehiculos_favoritos: Mapped[list["Vehiculo"]] = relationship(
        secondary=vehiculos_favoritos_tabla,
        back_populates="favorited_by"
    )

    planetas_favoritos: Mapped[list["Planeta"]] = relationship(
        secondary=planetas_favoritos_tabla,
        back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "tipo": self.tipo
        }
    
    
class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    raza: Mapped[str] = mapped_column(nullable=False)
    nacimiento: Mapped[str] = mapped_column(nullable=False)
    color_ojos: Mapped[str] = mapped_column(nullable=False)

    favorited_by: Mapped[list['User']] = relationship(
        secondary=personajes_favoritos_tabla,
        back_populates="personajes_favoritos"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "raza": self.raza,
            "nacimiento": self.nacimiento,
            "color_ojos": self.color_ojos
        }


class Vehiculo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    tamaño: Mapped[str] = mapped_column(nullable=False)
    peso: Mapped[str] = mapped_column(nullable=False)


    favorited_by: Mapped[list['User']] = relationship(
        secondary=vehiculos_favoritos_tabla,
        back_populates="vehiculos_favoritos"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "tamaño": self.tamaño,
            "peso": self.peso
        }


class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    tamaño: Mapped[str] = mapped_column(nullable=False)
    poblacion: Mapped[int] = mapped_column(nullable=False)

    favorited_by: Mapped[list['User']] = relationship(
        secondary=planetas_favoritos_tabla,
        back_populates="planetas_favoritos"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "tamaño": self.tamaño,
            "poblacion": self.poblacion
        }


"""
1. Declarar la tabla pivote. Relacionar dos tablas que seran muchos a muchos.
2. Comunicarle a ambos modelos que estaran relacionados mediante la tabla pivote
3. Indicarle a sqlalchemy que es la misma relacion, pero cada una cada cara de la misma moneda
user.personajes_favoritos <--> personajes.favorited_by
"""