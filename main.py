from fastapi import FastAPI

from database import engine
from models.base import Base
from routes import auth, song

# Create instance of FastAPI
app = FastAPI()

app.include_router(auth.router,prefix='/auth')
app.include_router(song.router,prefix='/song')

# Create all tables
Base.metadata.create_all(engine)

#to run first run .\virtenv\Scripts\activate
