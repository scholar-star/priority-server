from todos.total_todo.total_todo_service import TotalTodoService
from config_test import setup_database

import pytest

@pytest.mark.asyncio
async def test_total_delete_todo(setup_database):
    service = TotalTodoService()
    test_id = 1
    result = await service.delete_todo(test_id, setup_database)
    print(result)