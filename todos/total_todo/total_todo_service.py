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
        # 삭제할 Todo 항목을 조회
        todo = await db.execute(db.query(TodoRequest).filter(TodoRequest.id == todo_id).first())
        if todo:
            # Todo 항목과 관련된 SubTask 항목들을 먼저 삭제
            await db.execute(db.query(SubTask).filter(SubTask.task_id == todo_id).delete()) # 외부 DB와 통신하는 과정 - await
            await db.commit()
            # Todo 항목을 삭제
            await db.delete(todo)
            await db.commit()
            return {"message": f"Todo item with id {todo_id} deleted successfully."}
        else:
            return {"message": f"Todo item with id {todo_id} not found."}

    async def update_todo(self, todo_id: int, todo_update_dto: TodoRequest, db: AsyncSession):
        todo = await db.execute(db.query(TodoRequest).filter(TodoRequest.id == todo_id).first())
        if todo:
            if todo.due_date != todo_update_dto.due_date:
                # 마감 일자가 변경될 경우, 기존의 subtask들을 삭제하고 새로운 subtask들을 재분할.
                await db.execute(db.query(SubTask).filter(SubTask.task_id == todo_id).delete())
                await db.commit()
                subtasks = await self.divide_todo(todo_update_dto, db)
            else:
                # 마감 일자가 변경되지 않은 경우, 기존의 subtask들을 유지하고 업데이트된 todo 정보만 반영.
                todo.title = todo_update_dto.title
                todo.due_date = todo_update_dto.due_date
                await db.commit()
                await db.refresh(todo)
            return {"message": f"Todo item with id {todo_id} updated successfully.", "subtasks": subtasks}
        else:
            return {"message": f"Todo item with id {todo_id} not found."}

    async def divide_todo(self, todo_dto: TodoRequest, db: AsyncSession):
        result = await divide_and_submit(todo_dto)
        return result, result["subtasks"]