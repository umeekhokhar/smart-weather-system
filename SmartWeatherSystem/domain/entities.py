from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # In a real app, hash this!
    host_city = Column(String) # Feature: Host City

    # Feature: Individual History (One-to-Many)
    logs = relationship("WeatherLog", back_populates="user")

class WeatherLog(Base):
    __tablename__ = "weather_logs"

    weather_log_id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    condition = Column(String)
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    # Link log to a specific user
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="logs")