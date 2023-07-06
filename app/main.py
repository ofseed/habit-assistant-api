from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine
from app.dependencies import get_db
from app.routers import auth, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


app.include_router(auth.router)
app.include_router(users.router)
