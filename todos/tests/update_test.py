
import pytest

from config_test import setup_database
from insert_test import setup_user
from todos.total_todo.total_todo_service import TotalTodoService
from todos.total_todo.total_todo_dto import TodoRequest
from sqlalchemy import select
from infra.priority_db import SubTask, Task

@pytest.mark.asyncio
async def test_update_title(setup_database, setup_user):
    # 기존 Todo 항목 생성
    service = TotalTodoService()
    test_todo = TodoRequest(
        title="기술스펙 작성",
        due_date="2026-08-31"
    )
    insert_result = await service.insert_todo(setup_user.user_id, test_todo, setup_database)
    todo_id = insert_result["task_id"]

    # Todo 항목 업데이트
    updated_todo = TodoRequest(
        title="업데이트된 기술스펙 작성",
        due_date="2026-08-31"
    )
    update_result = await service.update_todo(todo_id, updated_todo, setup_database)

    # 업데이트 결과 확인
    assert update_result["message"] == f"Todo item with id {todo_id} updated successfully."

    # DB에서 업데이트된 항목 조회
    todo_query = select(Task).where(Task.task_id == todo_id)
    todo_result = await setup_database.execute(todo_query)
    updated_task = todo_result.scalar_one_or_none()

    assert updated_task is not None
    assert updated_task.title == "업데이트된 기술스펙 작성"

@pytest.mark.asyncio
async def test_update_date(setup_database, setup_user):
    # 기존 Todo 항목 생성
    service = TotalTodoService()
    test_todo = TodoRequest(
        title="기술스펙 작성",
        due_date="2026-08-31"
    )
    insert_result = await service.insert_todo(setup_user.user_id, test_todo, setup_database)
    todo_id = insert_result["task_id"]

    # Todo 항목 업데이트
    updated_todo = TodoRequest(
        title="기술스펙 작성",
        due_date="2026-09-15"
    )
    update_result = await service.update_todo(todo_id, updated_todo, setup_database)

    update_date_result = await setup_database.execute(select(SubTask).where(SubTask.task_id == todo_id))
    print("업데이트된 SubTask 항목들:", update_date_result.scalars().all())

    # 업데이트 결과 확인
    assert update_result["message"] == f"Todo item with id {todo_id} updated successfully."