from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.crud import get_user_by_username
from app.dependencies import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                              SECRET_KEY, get_db)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Annotated[Session, Depends(get_db)], user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(
    db: Annotated[Session, Depends(get_db)], username: str, password: str
):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/register/", response_model=schemas.User)
def register(db: Annotated[Session, Depends(get_db)], user: schemas.UserCreate):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    return create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
async def login(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
