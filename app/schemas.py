from datetime import time
from pydantic import BaseModel
from datetime import date


class Token(BaseModel):
    access_token: str
    token_type: str


class StatusBase(BaseModel):
    owner_id: int
    id: int
    start: time
    end: time
    date: date


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    pass

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    id: int
    owner_id: int
    gyroscopeX: float
    gyroscopeY: float
    gyroscopeZ: float
    accelerateX: float
    accelerateY: float
    accelerateZ: float
    screenStatus: bool
    latitude: float
    longitude: float
    time: time
    date: date


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    pass

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool
    status: list[Status] = []

    class Config:
        orm_mode = True
