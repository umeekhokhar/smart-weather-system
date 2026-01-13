from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)

    favorite_locations = relationship(
        "FavoriteLocation", back_populates="user"
    )

class FavoriteLocation(Base):
    __tablename__ = "favorite_locations"

    location_id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="favorite_locations")

class WeatherLog(Base):
    __tablename__ = "weather_logs"

    weather_log_id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    condition = Column(String)
    logged_at = Column(DateTime, default=datetime.utcnow)
