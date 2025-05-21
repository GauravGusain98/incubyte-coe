from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum

class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    due_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=True)
    priority = Column(Enum(PriorityEnum, name="priority_enum"), nullable=False, default=PriorityEnum("low"))

    assignee = relationship("User", back_populates="tasks", passive_deletes=True,  foreign_keys=[assignee_id])
    created_by = relationship("User", back_populates="created_tasks", passive_deletes=True, foreign_keys=[created_by_id])