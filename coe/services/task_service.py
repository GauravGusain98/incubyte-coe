from sqlalchemy.orm import Session
from coe.models.task import Task
from coe.schemas.task import CreateTaskRequestSchema, UpdateTaskRequestSchema

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

def get_tasks_list(db: Session) -> list[Task]:
    return db.query(Task).all()

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
