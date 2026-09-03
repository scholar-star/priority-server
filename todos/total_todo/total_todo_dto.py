
from pydantic import BaseModel

class TodoRequest(BaseModel):
    title: str
    due_date: str | None = None
    due_time: str | None = None
    total_time: int | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    due_date: str
    due_time: str