from infra.priority_db import SubTask
from sqlalchemy import select
from exception.custom_exceptions import DBNotFoundException

class SubTaskService:
    async def sub_task_done(subtask_id: int, db):
        # SubTask의 상태를 완료로 변경
        query = select(SubTask).where(SubTask.subtask_id == subtask_id)
        subtask = await db.execute(query)
        subtask = subtask.scalar_one_or_none()

        if subtask:
            subtask.complete = True
            await db.commit()
        else:
            raise DBNotFoundException(f"DB에서 이 할 일을 찾을 수 없어요.")
