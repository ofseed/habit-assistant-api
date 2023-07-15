from datetime import date, datetime, time

from pydantic import BaseModel

from app.models import StateType


class Token(BaseModel):
    access_token: str
    token_type: str


class StatusBase(BaseModel):
    start: time
    end: time
    date: date
    statusS: str


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    pass

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
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
    place: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int

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


class StateBase(BaseModel):
    start_time: datetime
    end_time: datetime
    state: StateType


class StateCreate(StateBase):
    pass


class State(StateBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
