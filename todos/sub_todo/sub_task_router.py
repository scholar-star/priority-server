
from fastapi import APIRouter, Depends
from infra.db_session import get_db
from sub_task_service import SubTaskService


router = APIRouter()

@router.patch("/sub_task/{id}/done")
async def sub_task_done(id: int, db = Depends(get_db)):
    return await SubTaskService.sub_task_done(id, db)
