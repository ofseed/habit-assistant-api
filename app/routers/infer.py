from app import schemas
from app.dependencies import get_current_active_user, get_db
from app.crud import *

from datetime import date, time, datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(prefix="/infer", tags=['infer'])

def infer(db: Session, user_id: int):
    pass

@router.post("/send-status")
async def receive_status(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    user_record: schemas.RecordCreate,
    background_task: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)]
):
    record_number = get_users_record_number(db, current_user.id)
    if 0 < record_number < 50:
        last_record = get_last_record(db, current_user.id)
        time_now = datetime.now()
        time_latest = datetime.combine(last_record.date, last_record.time)
        if (time_now - time_latest).seconds > 3600:
            background_task.add_task(infer, db, current_user.id)
        else:
            create_user_record(db, user_record, current_user.id)
    if record_number == 0:
        create_user_record(db, user_record, current_user.id)
    else:
        background_task.add_task(infer, db, current_user.id)

    return [{"msg": "success inject"}]



