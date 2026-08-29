
from fastapi import APIRouter, Depends
from infra.db_session import get_db
from total_todo_service import TotalTodoService
from total_todo_dto import TodoRequest

router = APIRouter()

@router.post("/todo/{user_id}/insert")
async def insert_todo(user_id: int, todo: TodoRequest, db = Depends(get_db)):
    return TotalTodoService().insert_todo(user_id, todo, db=Depends(get_db))

# Todo 전체 삭제
@router.delete("/todo/{id}/delete")
async def delete_todo(id: int, db = Depends(get_db)):
    return TotalTodoService().delete_todo(id, db)

@router.patch("/todo/{id}/update")
async def update_todo(id: int, todo: TodoRequest, db = Depends(get_db)):
    return TotalTodoService().update_todo(id, todo, db)
