from app import schemas
from app.dependencies import get_current_active_user, get_db
from app.crud import *

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(prefix="/infer", tags=['infer'])

#def stock_and_process

@router.post("/send-status")
async def receive_status(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    user_record: schemas.RecordCreate,
    background_task: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)]
):
    return [{"fuck you": get_users_record_number(db, 0)}]



