from fastapi import FastAPI
from fastapi.responses import JSONResponse
from custom_exceptions import DBNotFoundException

app = FastAPI()

@app.exception_handler(DBNotFoundException)
async def db_not_found_handler(request, exc: DBNotFoundException):
    return JSONResponse(
        status_code=500,
        content={"message": exc.message},
    )