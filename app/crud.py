from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete_users_record_all(db: Session, user_id: int):
    db.query(models.Record).filter(models.Record.owner_id == user_id).delete()
    db.commit()


def get_users_record_all(db: Session, user_id: int):
    return db.query(models.Record).filter(models.Record.owner_id == user_id).all()


def get_last_record(db: Session, user_id: int):
    return (
        db.query(models.Record)
        .filter(models.Record.owner_id == user_id)
        .order_by(desc(models.Record.time))
        .first()
    )


def get_earliest_record(db: Session, user_id: int):
    return (
        db.query(models.Record)
        .filter(models.Record.owner_id == user_id)
        .order_by(models.Record.time)
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_status(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Status).offset(skip).limit(limit).all()


def create_user_record(db: Session, record: schemas.RecordCreate, user_id: int):
    db_record = models.Record(**record.dict(), owner_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def create_user_status(db: Session, status: schemas.StatusCreate, user_id: int):
    db_status = models.Status(**status.dict(), owner_id=user_id)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def create_user_state(db: Session, state: schemas.StateCreate, user_id: int):
    db_state = models.State(**state.dict(), user_id=user_id)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


def get_user_states(db: Session, user_id: int, start_time: datetime, end_time: datetime):
    if start_time is None:
        start_time = datetime.fromtimestamp(0)
    if end_time is None:
        end_time = datetime.now()
    return (
        db.query(models.State)
        .filter(models.State.user_id == user_id)
        .filter(models.State.time >= start_time)
        .filter(models.State.time <= end_time)
        .all()
    )
