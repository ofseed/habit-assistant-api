import datetime as dt
from datetime import datetime
from typing import Annotated

import numpy as np
import torch
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import *
from app.dependencies import get_classifier, get_current_active_user, get_db
from app.models import Record, StateType
from app.utils.ContextAwareness import ContextFormer, ContextLSTM

router = APIRouter(prefix="/infer", tags=["infer"])

async def laplace(sensitivety, epsilon):
    n_value = np.random.laplace(0, sensitivety / epsilon, 1)
    return float(n_value)

async def transform_records_to_torch(records: Record):
    place_dict = {
        "食堂": [0, 0, 1, 0],
        "教室": [1, 0, 0, 0],
        "宿舍": [0, 1, 0, 0],
        "其他": [0, 0, 0, 1],
    }
    all_embeddings = []
    # to traverse each records, add it's parameter into list and convert list to tensor
    for record in records:
        one_embedding = [
            record.gyroscopeX,
            record.gyroscopeY,
            record.gyroscopeZ,
            record.accelerateX,
            record.accelerateY,
            record.accelerateZ,
            record.screenStatus,
            record.time.hour,
        ]
        one_embedding += place_dict[record.place]
        all_embeddings.append(one_embedding)
    # convert form
    all_embeddings = np.array(all_embeddings).astype("float32")
    all_embeddings = np.expand_dims(all_embeddings, axis=0)
    all_embeddings = torch.Tensor(all_embeddings)

    return all_embeddings


async def create_users_status(db: Session, user_id: int, status: StateType):
    last_record = get_last_record(db, user_id)
    earliest_record = get_earliest_record(db, user_id)
    end = last_record.time
    start = earliest_record.time
    end_date = last_record.date
    start_date = earliest_record.date

    end = datetime.combine(end_date, end)
    start = datetime.combine(earliest_record, start)

    for_create = schemas.StateCreate(start_time=start, end_time=end, state=status)
    create_user_state(db, for_create, user_id)


async def infer(db: Session, records: Record, user_id: int, model: ContextLSTM):
    status_dict = {5: StateType.LEARN, 4: StateType.COMMUTE,
                   3: StateType.SLEEP, 2: StateType.EAT,
                   1: StateType.EXERCISE, 0: StateType.LEISURE}

    # to get infer
    records_tensor = await transform_records_to_torch(records)
    output = model(records_tensor)
    index = torch.argmax(output)
    status = status_dict[int(index)]

    await create_users_status(db, user_id, status)

    # to delete cache of users record
    delete_users_record_all(db, user_id)


async def create_laplace_record(
    db: Session,
    user_record: schemas.RecordCreate,
    user_id: int
):
    user_record.accelerateX += await laplace(1, 10)
    user_record.accelerateY += await laplace(1, 10)
    user_record.accelerateZ += await laplace(1, 10)
    user_record.gyroscopeX += await laplace(1, 10)
    user_record.gyroscopeZ += await laplace(1, 10)
    user_record.gyroscopeY += await laplace(1, 10)
    create_user_record(db, user_record, user_id)

# get data, judge that whether user's status should be infered or not
@router.post("/send-status")
async def receive_status(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    user_record: schemas.RecordCreate,
    background_task: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)],
    model: Annotated[ContextLSTM, Depends(get_classifier)],
):
    records = get_users_record_all(db, current_user.id)
    record_number = len(records)

    # judge whether data need to be inferred, if his record number is  more than 6, deal it
    if 0 < record_number < 6:
        last_record = get_last_record(db, current_user.id)
        time_now = datetime.now()
        time_latest = datetime.combine(last_record.date, last_record.time)

        if (time_now - time_latest).seconds > 3600:
            delete_users_record_all(db, current_user.id)

        await create_laplace_record(db, user_record, current_user.id)

    elif record_number == 0:
        await create_laplace_record(db, user_record, current_user.id)
    else:
        background_task.add_task(infer, db, records, current_user.id, model)

    return [{"msg": "success inject", "data": 0}]
