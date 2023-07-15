from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_current_active_user, get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/me/status")
async def read_own_status(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return [{"status_id": "Foo", "owner": current_user.username}]


@router.get("/", response_model=list[schemas.User])
def read_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/status/", response_model=schemas.Status)
def create_status_for_user(
    db: Annotated[Session, Depends(get_db)], status: schemas.StatusCreate, user_id: int
):
    return crud.create_user_status(db=db, status=status, user_id=user_id)
