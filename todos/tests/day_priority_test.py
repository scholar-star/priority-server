from datetime import datetime

from todos.sub_todo.sub_priority import SubtaskPriority
from config_test import setup_database

import pytest

@pytest.mark.asyncio
async def test_day_priority(setup_database): # test_*로 시작하는 함수여야 pytest가 테스트 함수로 인식
    subtask_service = SubtaskPriority()

    target_date = "2026-08-31"
    result = await subtask_service.set_daily_subtask_priority(setup_database, target_date)
    print("테스트 완료")

    result = result.scalars().all()  # 결과를 리스트로 변환

    for subtask in result:
        print(subtask.__dict__)