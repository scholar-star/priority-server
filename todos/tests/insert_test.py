from config_test import setup_database
from todos.total_todo.total_todo_service import TotalTodoService
from todos.total_todo.total_todo_dto import TodoRequest, TodoResponse

import pytest

@pytest.mark.asyncio
async def test_insert(setup_database):
    test_todo = TodoRequest(
        title="기술스펙 작성",
        due_date="2026-08-31"
    )
    
    service = TotalTodoService()
    result = await service.insert_todo(1, test_todo, setup_database)
    print(result)

