from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

# Tablas intermedias para las relaciones muchos a muchos (favoritos)
favorite_planets = db.Table('favorite_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

favorite_characters = db.Table('favorite_characters',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

favorite_vehicles = db.Table('favorite_vehicles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    
    # Relaciones
    favorite_planets: Mapped[list["Planet"]] = relationship(
        "Planet", 
        secondary=favorite_planets,
        back_populates="fans"
    )
    favorite_characters: Mapped[list["Character"]] = relationship(
        "Character", 
        secondary=favorite_characters,
        back_populates="fans"
    )
    favorite_vehicles: Mapped[list["Vehicle"]] = relationship(
        "Vehicle", 
        secondary=favorite_vehicles,
        back_populates="fans"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    diameter: Mapped[int] = mapped_column(Integer, nullable=True)
    rotation_period: Mapped[int] = mapped_column(Integer, nullable=True)
    orbital_period: Mapped[int] = mapped_column(Integer, nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    surface_water: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Relaciones
    characters: Mapped[list["Character"]] = relationship(
        "Character", 
        back_populates="home_planet",
        cascade="all, delete-orphan"
    )
    fans: Mapped[list["User"]] = relationship(
        "User", 
        secondary=favorite_planets,
        back_populates="favorite_planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "surface_water": self.surface_water
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    mass: Mapped[int] = mapped_column(Integer, nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Foreign Keys
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=True)
    
    # Relaciones
    home_planet: Mapped["Planet"] = relationship("Planet", back_populates="characters")
    species: Mapped["Species"] = relationship("Species", back_populates="characters")
    fans: Mapped[list["User"]] = relationship(
        "User", 
        secondary=favorite_characters,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "planet_id": self.planet_id,
            "species_id": self.species_id
        }

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=True)
    cost_in_credits: Mapped[int] = mapped_column(Integer, nullable=True)
    length: Mapped[float] = mapped_column(Float, nullable=True)
    max_atmosphering_speed: Mapped[int] = mapped_column(Integer, nullable=True)
    crew: Mapped[int] = mapped_column(Integer, nullable=True)
    passengers: Mapped[int] = mapped_column(Integer, nullable=True)
    cargo_capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    consumables: Mapped[str] = mapped_column(String(100), nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Relaciones
    fans: Mapped[list["User"]] = relationship(
        "User", 
        secondary=favorite_vehicles,
        back_populates="favorite_vehicles"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class
        }

class Species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    classification: Mapped[str] = mapped_column(String(100), nullable=True)
    designation: Mapped[str] = mapped_column(String(100), nullable=True)
    average_height: Mapped[int] = mapped_column(Integer, nullable=True)
    average_lifespan: Mapped[int] = mapped_column(Integer, nullable=True)
    hair_colors: Mapped[str] = mapped_column(String(200), nullable=True)
    skin_colors: Mapped[str] = mapped_column(String(200), nullable=True)
    eye_colors: Mapped[str] = mapped_column(String(200), nullable=True)
    language: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Relaciones
    characters: Mapped[list["Character"]] = relationship(
        "Character", 
        back_populates="species",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "eye_colors": self.eye_colors,
            "language": self.language
        }