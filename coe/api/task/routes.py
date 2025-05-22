from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from coe.db.session import SessionLocal
from coe.services.auth_service import get_current_user
from coe.services.task_service import create_task, find_task_by_id, update_task_details, remove_task
from coe.schemas.task import CreateTaskRequestSchema, CreateTaskResponseSchema, GetTaskResponseSchema, ErrorResponse, UpdateTaskRequestSchema, UpdateTaskResponseSchema, DeleteTaskResponseSchema

router = APIRouter(tags=["Tasks"], prefix="/task", dependencies=[Depends(get_current_user)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/add",
    summary="Create a new task",
    response_model=CreateTaskResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create(task_data: CreateTaskRequestSchema, db: Session = Depends(get_db)):
    new_task = create_task(task_data, db)
    
    return {"message": "Task created successfully", "task_id": new_task.id}

@router.get(
    "/{task_id}", 
    summary="Fetch a task by ID",
    response_model=GetTaskResponseSchema,
    responses={404: {"model": ErrorResponse}}
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = find_task_by_id(task_id, db)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    
    return task

@router.put(
    "/{task_id}", 
    summary="Update a task details",
    response_model=UpdateTaskResponseSchema,
    responses={404: {"model": ErrorResponse}}
)
def update_task(task_id: int, task_data: UpdateTaskRequestSchema, db: Session = Depends(get_db)):
    success = update_task_details(task_id, task_data, db)
    
    if success:
        return {"message": "Task data updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
@router.delete(
    "/{task_id}",
    summary="Remove a task by ID",
    response_model=DeleteTaskResponseSchema,
    responses={404: {"model": ErrorResponse}}
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = remove_task(task_id, db)
    if success:
        return {"message": "Task removed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )