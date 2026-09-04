from infra.priority_db import SubTask
from sqlalchemy import select
from exception.custom_exceptions import DBNotFoundException
from todos.ai.divide_ai import adjust_subtask

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

    async def insert_sub_task(sub_task_dto, db):
        total_task_id = sub_task_dto.total_task_id
        query = select(SubTask).where(SubTask.task_id == total_task_id)

        subtasks = await db.execute(query)
        subtasks = subtasks.scalars().all()

        # 새로운 SubTask를 추가할 때, 기존 SubTask들의 order와 비율을 고려하여 새로운 SubTask를 추가
        subtasks.append(sub_task_dto)
        adjusted_subtasks = await adjust_subtask([sub_task.model_dump() for sub_task in subtasks])

        # 기존 SubTask들을 삭제하고, 조정된 SubTask들을 다시 추가
        for subtask in subtasks:
            await db.delete(subtask)

        for subtask_data in adjusted_subtasks:
            new_subtask = SubTask(
                task_id=total_task_id,
                subtask_title=subtask_data["subtask_title"],
                ratio=subtask_data["ratio"],
                urgent=subtask_data["urgent"],
                importance=subtask_data["importance"],
                order=subtask_data["order"],
                scheduled_date=subtask_data.get("date"),
                estimated_time=subtask_data.get("estimated_time"),
                complete=False
            )
            db.add(new_subtask)
        await db.commit()

        return {"message": "SubTask inserted and adjusted successfully.", "subtasks": adjusted_subtasks}

