from total_todo_dto import TodoRequest, TodoResponse
from infra.priority_db import User, Task, SubTask
from todos.ai.divide_ai import divide_and_submit
from sqlalchemy.orm import Session

class TotalTodoService:
    def insert_todo(self, todo_insert_dto:TodoRequest, db:Session):
        result, subtasks = divide_and_submit(todo_insert_dto)
        new_task = Task(
            title=result["task_name"],
            deadline=result["deadline"],
            status="pending",
            total_estimated=result["total_estimated"],
            is_fixed=False
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        for subtask in subtasks:
            new_subtask = SubTask(
                task_id=new_task.task_id,
                subtask_title=subtask["subtask_title"],
                ratio=subtask["ratio"],
                urgent=subtask["urgent"],
                importance=subtask["importance"],
                order=subtask["order"],
                scheduled_date=subtask.get("scheduled_date"),
                estimated_time=subtask.get("estimated_time"),
                complete=False
            )
            db.add(new_subtask)
        db.commit()
        return {"message": "Todo item inserted successfully.", "task_id": new_task.task_id, "subtasks": subtasks}
    
    def delete_todo(self, todo_id: int, db:Session):
        # 삭제할 Todo 항목을 조회
        todo = db.query(TodoRequest).filter(TodoRequest.id == todo_id).first()
        if todo:
            # Todo 항목과 관련된 SubTask 항목들을 먼저 삭제
            db.query(SubTask).filter(SubTask.task_id == todo_id).delete()
            db.commit()
            # Todo 항목을 삭제
            db.delete(todo)
            db.commit()
            return {"message": f"Todo item with id {todo_id} deleted successfully."}
        else:
            return {"message": f"Todo item with id {todo_id} not found."}

    def update_todo(self, todo_id: int, todo_update_dto: TodoRequest, db: Session):
        todo = db.query(TodoRequest).filter(TodoRequest.id == todo_id).first()
        if todo:
            if todo.due_date != todo_update_dto.due_date:
                # 마감 일자가 변경될 경우, 기존의 subtask들을 삭제하고 새로운 subtask들을 재분할.
                db.query(SubTask).filter(SubTask.task_id == todo_id).delete()
                db.commit()
                subtasks = self.divide_todo(todo_id, db)
            else:
                # 마감 일자가 변경되지 않은 경우, 기존의 subtask들을 유지하고 업데이트된 todo 정보만 반영.
                todo.title = todo_update_dto.title
                todo.due_date = todo_update_dto.due_date
                db.commit()
                db.refresh(todo)
            return {"message": f"Todo item with id {todo_id} updated successfully.", "subtasks": subtasks}
        else:
            return {"message": f"Todo item with id {todo_id} not found."}

    def divide_todo(self, todo_dto: TodoRequest, db: Session):
        result = divide_and_submit(todo_dto)
        return result, result["subtasks"]