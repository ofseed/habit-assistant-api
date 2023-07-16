from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, infer, users

_ = load_dotenv(find_dotenv())

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(infer.router)
