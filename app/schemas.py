from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
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
    items: list[Item] = []

    class Config:
        orm_mode = True
