from sqlalchemy.orm import Session
from infra.priority_db import SubTask
from sqlalchemy.ext.asyncio import AsyncSession
class SubtaskPriority:
    async def set_daily_subtask_priority(self, db: AsyncSession, date: str):
        # 하루 동안의 subtask들을 조회하고, urgent와 importance를 기준으로 우선순위를 설정
        subtasks = await db.execute(db.query(SubTask).filter(SubTask.scheduled_date == date))
        subtasks = subtasks.scalars().all() # 비동기 전체 조회
        subtasks.sort(key=lambda x: (x.urgent+x.importance), reverse=True)
        return subtasks