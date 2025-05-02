from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Float, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


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
        data['made_by_teacher'] = self.made_by_teacher.serialize()
        data['students'] = [student.serialize() for student in self.students]
        return data


class Planeta(db.Model):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    diametro: Mapped[int] = mapped_column(Integer, nullable=True)
    clima: Mapped[str] = mapped_column(String(50), nullable=True)
    poblacion: Mapped[int] = mapped_column(Integer, nullable=True)
    imagen_url: Mapped[str] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)

    personajes = relationship("Personaje", back_populates="planeta_natal")
    favoritos = relationship("PlanetaFavorito", back_populates="planeta")

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
        data['made_by_teacher'] = self.made_by_teacher.serialize()
        data['students'] = [student.serialize() for student in self.students]
        return data


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
    planeta_natal_id: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"),unique = True, nullable=True)

    vehiculo = relationship("Vehiculo", back_populates="personaje", uselist=False)
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
        data['made_by_teacher'] = self.made_by_teacher.serialize()
        data['students'] = [student.serialize() for student in self.students]
        return data


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
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personajes.id"), nullable=True)

    personaje = relationship("Personaje", back_populates="vehiculo", uselist=False)
    favoritos = relationship("VehiculoFavorito", back_populates="vehiculo")

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
            "descripcion": self.descripcion
        }
    def serialize_with_relations(self):
        data = self.serialize()
        data['made_by_teacher'] = self.made_by_teacher.serialize()
        data['students'] = [student.serialize() for student in self.students]
        return data





class PlanetaFavorito(db.Model):
    __tablename__ = "planetas_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    usuario = relationship("Usuario", back_populates="planetas_favoritos")
    planeta = relationship("Planeta", back_populates="favoritos")
    

class PersonajeFavorito(db.Model):
    __tablename__ = "personajes_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personajes.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    usuario = relationship("Usuario", back_populates="personajes_favoritos")
    personaje = relationship("Personaje", back_populates="favoritos")


class VehiculoFavorito(db.Model):
    __tablename__ = "vehiculos_favoritos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    usuario = relationship("Usuario", back_populates="vehiculos_favoritos")
    vehiculo = relationship("Vehiculo", back_populates="favoritos")
