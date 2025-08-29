from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha_subscripcion: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=True)
    apellido: Mapped[str] = mapped_column(String(80), nullable=True)

    # relationships to favorite association objects
    planetas_favoritos = relationship(
        "PlanetaFavorito", back_populates="usuario", cascade="all, delete-orphan")
    personajes_favoritos = relationship(
        "PersonajeFavorito", back_populates="usuario", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fecha_subscripcion": self.fecha_subscripcion.isoformat() if self.fecha_subscripcion else None,
            "nombre": self.nombre,
            "apellido": self.apellido,
        }


class Planeta(db.Model):
    __tablename__ = "planeta"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    favoritos = relationship(
        "PlanetaFavorito", back_populates="planeta", cascade="all, delete-orphan")

    def serialize(self):
        return {"id": self.id, "nombre": self.nombre}


class Personaje(db.Model):
    __tablename__ = "personaje"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    favoritos = relationship(
        "PersonajeFavorito", back_populates="personaje", cascade="all, delete-orphan")

    def serialize(self):
        return {"id": self.id, "nombre": self.nombre}


class PlanetaFavorito(db.Model):
    __tablename__ = "planeta_favorito"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(
        ForeignKey("planeta.id"), nullable=False)
    fecha_agregado: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="planetas_favoritos")
    planeta = relationship("Planeta", back_populates="favoritos")

    def serialize(self):
        return {"id": self.id, "usuario_id": self.usuario_id, "planeta_id": self.planeta_id, "fecha_agregado": self.fecha_agregado.isoformat()}


class PersonajeFavorito(db.Model):
    __tablename__ = "personaje_favorito"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(
        ForeignKey("personaje.id"), nullable=False)
    fecha_agregado: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="personajes_favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")

    def serialize(self):
        return {"id": self.id, "usuario_id": self.usuario_id, "personaje_id": self.personaje_id, "fecha_agregado": self.fecha_agregado.isoformat()}
