from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
    Time,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    states = relationship("State", back_populates="user")
    statistics = relationship("Statistics", back_populates="user")

    status = relationship("Status", back_populates="owner")
    record = relationship("Record", back_populates="owner")


class StateType(PyEnum):
    LEARN = "学习"
    COMMUTE = "通勤"
    SLEEP = "睡觉"
    EAT = "吃饭"
    EXERCISE = "运动"
    LEISURE = "摸鱼"


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    state = Column(Enum(StateType))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="states")


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Enum(StateType))
    total_time = Column(Interval)
    date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="statistics")


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(Time)
    end = Column(Time)
    date = Column(Date)
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
    time = Column(Time)
    date = Column(Date)
    place = Column(String)

    owner = relationship("User", back_populates="record")
