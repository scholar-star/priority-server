import pytest_asyncio
from sqlalchemy import select

from config_test import setup_database
from infra.priority_db import User
from todos.total_todo.total_todo_service import TotalTodoService
from todos.total_todo.total_todo_dto import TodoRequest

import pytest

@pytest_asyncio.fixture(scope="function")
async def setup_user(setup_database):
    # 테스트용 사용자 생성
    user_query = select(User).where(User.email == "test@test.com")
    user_result = await setup_database.execute(user_query)
    test_user = user_result.scalar_one_or_none()

    if test_user:
        return test_user
    
    test_user = User(
        oauth_id="test_oauth_id",
        nickname="test_user",
        email="test@test.com"
    )
    setup_database.add(test_user)

    await setup_database.flush()
    await setup_database.refresh(test_user)  # test_user 객체를 새로고침하여 user_id를 가져옴
    return test_user

@pytest.mark.asyncio
async def test_insert(setup_database, setup_user):
    test_todo = TodoRequest(
        title="기술스펙 작성",
        due_date="2026-08-31"
    )
    
    service = TotalTodoService()
    result = await service.insert_todo(setup_user.user_id, test_todo, setup_database)
    print(result)

