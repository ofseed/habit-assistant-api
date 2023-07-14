from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users_record_number(db: Session, user_id: int):
    return len(db.query(models.Record).filter(models.Record.owner_id == user_id))


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_status(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Status).offset(skip).limit(limit).all()


def create_user_status(db: Session, status: schemas.StatusCreate, user_id: int):
    db_status = models.Status(**status.dict(), owner_id=user_id)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status
