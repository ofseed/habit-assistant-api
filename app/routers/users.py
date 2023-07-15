from datetime import date
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


@router.get("/me/states/", response_model=list[schemas.State])
async def read_own_states(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    start_date: date = None,
    end_date: date = None,
):
    return crud.get_user_states(db=db, user_id=current_user.id, start_date=start_date, end_date=end_date)


@router.post("/me/states/", response_model=schemas.State)
async def create_state_for_user(
    db: Annotated[Session, Depends(get_db)],
    state: schemas.StateCreate,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return crud.create_user_state(db=db, state=state, user_id=current_user.id)


@router.get("/me/statistics/", response_model=schemas.Statistics)
async def read_own_statistics(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    start_date: date = None,
    end_date: date = None,
):
    return crud.get_user_statistics(db=db, user_id=current_user.id, start_date=start_date, end_date=end_date)


@router.post("/me/statistics/", response_model=schemas.Statistics)
async def create_statistics_for_user(
    db: Annotated[Session, Depends(get_db)],
    statistics: schemas.StatisticsCreate,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return crud.create_user_statistics(db=db, statistics=statistics, user_id=current_user.id)


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
