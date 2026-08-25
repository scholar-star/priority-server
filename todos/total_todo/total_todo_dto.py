
from pydantic import BaseModel

class TodoRequest(BaseModel):
    title: str
    due_date: str

class TodoResponse(BaseModel):
    id: int
    title: str
    due_date: str