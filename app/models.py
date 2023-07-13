from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    status = relationship("Item", back_populates="owner")


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime)
    end = Column(DateTime)
    statusS = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="status")


class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    gyroscopeX = Column(Float)
    gyroscopeY = Column(Float)
    gyroscopeZ = Column(Float)
    accelerateX = Column(Float)
    accelerateY = Column(Float)
    accelerateZ = Column(Float)
    screenStatus = Column(Boolean)
    latitude = Column(Float)
    longitude = Column(Float)
    time = Column(DateTime)

    owner = relationship("User", back_populates="record")
