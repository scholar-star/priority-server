
from pydantic import BaseModel

class SubTaskRequest(BaseModel):
    sub_task_title: str
    total_task_id: int
