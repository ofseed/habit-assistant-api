from app import schemas
from app.dependencies import get_current_active_user

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated




router = APIRouter(prefix="infer", tags=['infer'])

@router.post("/send-status")
async def receive_status(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    user_record: schemas.RecordBase
):
    pass

