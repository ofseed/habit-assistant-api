import numpy as np
import torch

from app import schemas
from app.dependencies import get_current_active_user, get_db, get_classifier
from app.crud import *
from app.models import Record
from app.utils.ContextAwareness import ContextLSTM, ContextFormer

from datetime import date, time, datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/infer", tags=['infer'])

async def transform_records_to_torch(
        records: Record
):
    place_dict = {"食堂": [0, 0, 1, 0], "教室": [1, 0, 0, 0], "宿舍": [0, 1, 0, 0],
                  "其他": [0, 0, 0, 1]}
    all_embeddings = []
    for record in records:
        one_embedding = [record.gyroscopeX, record.gyroscopeY, record.gyroscopeZ,
                         record.accelerateX, record.accelerateY, record.accelerateZ,
                         record.screenStatus, record.time.hour, record.time.minute,
                         record.time.second]
        one_embedding += place_dict[record.place]
        all_embeddings.append(one_embedding)
    all_embeddings = np.array(all_embeddings).astype("float32")
    all_embeddings = torch.Tensor(all_embeddings)
    return all_embeddings


async def infer(
        records: Record,
        user_id: int,
        model: ContextLSTM
):
    pass


@router.post("/send-status")
async def receive_status(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        user_record: schemas.RecordCreate,
        background_task: BackgroundTasks,
        db: Annotated[Session, Depends(get_db)],
        model: Annotated[ContextLSTM, Depends(get_classifier)]
):
    records = get_users_record_all(db, current_user.id)
    record_number = len(records)
    if 0 < record_number < 6:
        last_record = get_last_record(db, current_user.id)
        time_now = datetime.now()
        time_latest = datetime.combine(last_record.date, last_record.time)
        if (time_now - time_latest).seconds > 3600:
            background_task.add_task(infer, records, current_user.id, model)
        else:
            create_user_record(db, user_record, current_user.id)
    if record_number == 0:
        create_user_record(db, user_record, current_user.id)
    else:
        background_task.add_task(infer, records, current_user.id, model)
    return [{"msg": "success inject", "data": 0}]
