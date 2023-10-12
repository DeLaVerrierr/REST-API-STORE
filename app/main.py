from database.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
import logging
from api import user


app = FastAPI()


app.include_router(user.router, prefix="/api/v1/store", tags=["user"])
