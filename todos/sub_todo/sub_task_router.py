
from fastapi import APIRouter, Depends
from infra.db_session import get_db
from sub_task_service import SubTaskService
from sub_task_dto import SubTaskRequest

router = APIRouter()

@router.patch("/sub_task/{id}/done")
async def sub_task_done(id: int, db = Depends(get_db)):
    return await SubTaskService.sub_task_done(id, db)

@router.post("/sub_task/insert")
async def insert_sub_task(sub_task: SubTaskRequest, db = Depends(get_db)):
    return await SubTaskService.insert_sub_task(sub_task, db)

