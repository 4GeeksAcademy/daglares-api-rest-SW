from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "name": self.name,
            "terrain": self.terrain,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    mass: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "name": self.name,
            "mass": self.mass,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class Planets_favorites(db.Model):
    __tablename__ = "planets_favorites"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_ID: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship()

    planets_ID: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planets: Mapped["Planets"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_ID": self.user_ID,
            "planets_ID": self.planets_ID,
        }


class People_favorites(db.Model):
    __tablename__ = "people_favorites"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_ID: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship()

    people_ID: Mapped[int] = mapped_column(ForeignKey('people.id'))
    people: Mapped["People"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_ID": self.user_ID,
            "people_ID": self.people_ID,
        }
