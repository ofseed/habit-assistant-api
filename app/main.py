from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine
from app.dependencies import get_db
from app.routers import auth, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/status/", response_model=list[schemas.Status])
def read_status(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    status = crud.get_status(db, skip=skip, limit=limit)
    return status


app.include_router(auth.router)
app.include_router(users.router)
