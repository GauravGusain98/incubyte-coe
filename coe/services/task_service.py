from sqlalchemy.orm import Session
from coe.models.task import Task
from coe.schemas.task import CreateTaskRequestSchema, UpdateTaskRequestSchema, TaskFilters
from typing import List, Tuple
from sqlalchemy import or_, func

def create_task(task_data: CreateTaskRequestSchema, db: Session) -> Task:
    db_task = Task(
        name=task_data.name,
        description=task_data.description,
        created_by_id=1,
        assignee_id=task_data.assignee_id,
        due_date=task_data.due_date,
        start_date=task_data.start_date,
        priority=task_data.priority
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

def find_task_by_id(task_id: int, db: Session) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

def apply_task_filters(queryset, filters: TaskFilters):
    if filters.status:
        queryset = queryset.filter(Task.status == filters.status)

    if filters.priority:
        queryset = queryset.filter(Task.priority == filters.priority)

    if filters.search:
        search_term = f"%{filters.search.lower()}%"
        queryset = queryset.filter(
            or_(
                func.lower(Task.name).like(search_term),
                func.lower(Task.description).like(search_term)
            )
        )

    return queryset

def get_tasks_list(db: Session, filters: TaskFilters, skip: int = 0, limit: int = 10,) -> Tuple[List[Task], int]:
    queryset = db.query(Task)
    queryset = apply_task_filters(queryset, filters)
    total = queryset.count()
    tasks = queryset.offset(skip).limit(limit).all()

    return (tasks, total)

def get_total_tasks(db: Session) -> int:
    return db.query(Task).count()

def update_task_details(task_id:int, task_data: UpdateTaskRequestSchema, db: Session) -> bool:
    task = db.query(Task).filter_by(id=task_id).first()

    if not task:
        return False

    # Use dict and setattr to dynamically update only non-None fields
    update_fields = task_data.model_dump(exclude_unset=True, exclude={"id"})
    for field, value in update_fields.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task) 

    return True

def remove_task(task_id: int, db: Session) -> bool:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()

        return True
    
    return False
