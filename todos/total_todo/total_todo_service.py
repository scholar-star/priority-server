from sqlalchemy import delete, select

from .total_todo_dto import TodoRequest
from infra.priority_db import Task, SubTask
from todos.ai.divide_ai import divide_and_submit
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

class TotalTodoService:
    async def insert_todo(self, user_id: int, todo_insert_dto:TodoRequest, db:AsyncSession):
        result, subtasks = await self.divide_todo(todo_insert_dto, db)
        new_task = Task(
            user_id=user_id,
            title=result["task_name"],
            deadline=datetime.datetime.strptime(result["deadline"], "%Y-%m-%d"),
            status="pending",
            total_estimated=result["total_estimated"],
            is_fixed=False
        )
        db.add(new_task) # DB에 추가하는 방식이 아닌, ORM 객체를 생성하고 세션에 추가하는 방식.
        await db.flush()

        new_task_id = new_task.task_id

        for subtask in subtasks:
            new_subtask = SubTask(
                task_id=new_task_id,
                subtask_title=subtask["subtask_title"],
                ratio=subtask["ratio_percent"],
                urgent=result["urgency"],
                importance=result["importance"],
                order=subtask["order"],
                scheduled_date=datetime.datetime.strptime(subtask.get("date"), "%Y-%m-%d") if subtask.get("date") else None,
                estimated_time=subtask.get("estimated_time"),
                complete=False
            )
            db.add(new_subtask)
        await db.commit()
        return {"message": "Todo item inserted successfully.", "task_id": new_task_id, "subtasks": subtasks}

    async def delete_todo(self, todo_id: int, db:AsyncSession):
        todo_query = (
            select(Task)
            .where(Task.task_id == todo_id)
        )
        # 삭제할 Todo 항목을 조회
        todo = await db.execute(todo_query)
        todo = todo.scalar_one_or_none()
        if todo:
            # Todo 항목과 관련된 SubTask 항목들을 먼저 삭제
            subtasks_query = (
                select(SubTask)
                .where(SubTask.task_id == todo_id)
            )
            subtasks = await db.execute(subtasks_query)
            subtasks = subtasks.scalars().all()
            for subtask in subtasks:
                await db.delete(subtask)
            await db.commit()
            # Todo 항목을 삭제
            await db.delete(todo)
            await db.commit()
            return {"message": f"Todo item with id {todo_id} deleted successfully."}
        else:
            return {"message": f"Todo item with id {todo_id} not found."}

    async def update_todo(self, todo_id: int, todo_update_dto: TodoRequest, db: AsyncSession):
        todo_query = (
            select(Task)
            .where(Task.task_id == todo_id)
        )

        old_todo = await db.execute(todo_query)
        old_todo = old_todo.scalar_one_or_none()
        if todo_update_dto.title != old_todo.title:
            old_todo.title = todo_update_dto.title
        if todo_update_dto.due_date != old_todo.deadline or todo_update_dto.due_time != old_todo.due_time:
            old_todo.deadline = datetime.datetime.strptime(todo_update_dto.due_date, "%Y-%m-%d")
            subtasks_query = (
                delete(SubTask)
                .where(SubTask.task_id == todo_id)
            )
            await db.execute(subtasks_query) # 삭제 쿼리를 실행하는 것이기 때문에, 삭제 이후의 데이터는 남아있지 않다. 

            divide_result, subtasks = await self.divide_todo(todo_update_dto, db)
            for subtask in subtasks:
                new_subtask = SubTask(
                    task_id=todo_id,
                    subtask_title=subtask["subtask_title"],
                    ratio=subtask["ratio_percent"],
                    urgent=divide_result["urgency"],
                    importance=divide_result["importance"],
                    order=subtask["order"],
                    scheduled_date=datetime.datetime.strptime(subtask.get("date"), "%Y-%m-%d") if subtask.get("date") else None,
                    estimated_time=subtask.get("estimated_time"),
                    complete=False
                )
                db.add(new_subtask)
        await db.commit()
        return {"message": f"Todo item with id {todo_id} updated successfully."}

    async def divide_todo(self, todo_dto: TodoRequest, db: AsyncSession):
        result = await divide_and_submit(todo_dto)
        return result, result["subtasks"]