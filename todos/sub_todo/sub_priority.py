import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from infra.priority_db import SubTask
from sqlalchemy.ext.asyncio import AsyncSession

import datetime
class SubtaskPriority:
    async def set_daily_subtask_priority(self, db: AsyncSession, date: str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        # 하루 동안의 subtask들을 조회하고, urgent와 importance를 기준으로 우선순위를 설정
        query = (
            select(SubTask)
            .where(SubTask.scheduled_date == date)
            .order_by((SubTask.urgent + SubTask.importance).desc())
        )

        subtasks = await db.execute(query)
        return subtasks