from sqlalchemy.orm import Session
from infra.priority_db import SubTask

class SubtaskPriority:
    def set_daily_subtask_priority(self, db: Session, date: str):
        # 하루 동안의 subtask들을 조회하고, urgent와 importance를 기준으로 우선순위를 설정
        subtasks = db.query(SubTask).filter(SubTask.scheduled_date == date).all()
        subtasks.sort(key=lambda x: (x.urgent+x.importance), reverse=True)
        return subtasks