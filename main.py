from fastapi import FastAPI
from infra.priority_db import Base
from infra.db_session import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}