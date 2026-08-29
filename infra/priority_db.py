from datetime import datetime, date
from typing import List
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    # Columns
    user_id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    oauth_id : Mapped[str] = mapped_column(String, unique=True)
    email : Mapped[str] = mapped_column(String, unique=True)
    nickname : Mapped[str] = mapped_column(String(50), nullable=False)
    # Relationships
    tasks : Mapped[List["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    # Columns
    task_id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    title : Mapped[str] = mapped_column(String(200), nullable=False)
    deadline : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status : Mapped[str] = mapped_column(String(50), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_estimated : Mapped[int] = mapped_column(Integer, nullable=True)
    is_fixed : Mapped[bool] = mapped_column(Boolean, default=False)
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tasks")
    subtasks: Mapped[List["SubTask"]] = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")

class SubTask(Base):
    __tablename__ = "subtasks"
    # Columns
    subtask_id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id : Mapped[int] = mapped_column(Integer, ForeignKey("tasks.task_id"))
    subtask_title : Mapped[str] = mapped_column(String(200), nullable=False)
    ratio : Mapped[float] = mapped_column(String(50), nullable=False)
    urgent : Mapped[int] = mapped_column(Integer, default=3)
    importance : Mapped[int] = mapped_column(Integer, nullable=False)
    order : Mapped[int] = mapped_column(Integer, nullable=False)
    scheduled_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    estimated_time : Mapped[int] = mapped_column(Integer, nullable=True)
    complete : Mapped[bool] = mapped_column(Boolean, default=False)
    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="subtasks")
