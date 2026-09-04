
from pydantic import BaseModel

class SubTaskRequest(BaseModel):
    sub_task_title: str
    total_task_id: int

class SubTaskResponse(BaseModel):
    subtask_id: int
    date: str
    subtask_title: str
    total_task_id: int
    ratio: int
    estimated_time: int
    urgent: float
    importance: float
    complete: bool

