from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as pyEnum

db = SQLAlchemy()


# class FavoritesEnum(pyEnum):
#     PLANETS = "planets"
#     PEOPLE = "people"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites = relationship(
        'Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    favorites = relationship(
        "Favorite", back_populates="people")

    def serialize_people(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    favorites: Mapped[list['Favorite']] = relationship(
        "Favorite", back_populates="planet")

    def serialize_planets(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    # favorite: Mapped[FavoritesEnum] = mapped_column(
    #     Enum(FavoritesEnum, name="favorites_enum"))
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=True)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'),nullable=True)
    user = relationship(
        "User", back_populates="favorites")
    planet = relationship(
        "Planets", back_populates="favorites")
    people = relationship(
        "People", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            # "favorite": self.favorite.value,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
