from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class StatusBase(BaseModel):
    owner_id: int
    description: str | None = None


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int
    owner_id: int

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
