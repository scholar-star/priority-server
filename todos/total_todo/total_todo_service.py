from total_todo_dto import TodoRequest, TodoResponse
from infra.priority_db import User, Task, SubTask
from sqlalchemy.orm import Session

class TotalTodoService:
    def insert_todo(self, todo_insert_dto:TodoRequest, db:Session):
        new_todo = Task(
            title=todo_insert_dto.title,
            deadline=todo_insert_dto.due_date
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        response = TodoResponse(id=new_todo.id, title=new_todo.title, due_date=new_todo.due_date)
        subtasks = self.divide_todo(new_todo.id, db)
        result = {
            "message": "Todo item inserted successfully.",
            "todo": response,
            "subtasks": subtasks
        }
        return result
    
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

    def divide_todo(self, todo_id: int, db: Session):
        todo = db.query(TodoRequest).filter(TodoRequest.id == todo_id).first()
        sub_todos = []
        # AI를 통해 todo를 여러 개의 subtask로 나누는 로직 구현 예정
        return sub_todos