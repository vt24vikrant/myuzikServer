from fastapi import FastAPI

from database import engine
from models.base import Base
from routes import auth

# Create instance of FastAPI
app = FastAPI()

app.include_router(auth.router,prefix='/auth')

# Create all tables
Base.metadata.create_all(engine)

#to run first run .\virtenv\Scripts\activate
