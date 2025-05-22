from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from coe.db.session import SessionLocal
from coe.services.auth_service import get_current_user
from coe.services.task_service import create_task, find_task_by_id, update_task_details, remove_task, get_tasks_list, get_total_tasks
from coe.schemas.task import CreateTaskRequestSchema, CreateTaskResponseSchema, GetTaskResponseSchema, ErrorResponse, UpdateTaskRequestSchema, UpdateTaskResponseSchema, DeleteTaskResponseSchema, GetTaskListResponseSchema, TaskFilters
import math

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
    "/list",
    summary="Get all the tasks",
    response_model=GetTaskListResponseSchema,
)
def get_task_list(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    records_per_page: int = Query(10, le=100, description="Number of items per page"),
    filters: TaskFilters = Depends()
):
    skip = (page - 1) * records_per_page
    tasks, total_records = get_tasks_list(db, filters, skip=skip, limit=records_per_page)
    
    return {
        "message": "Task fetched successfully",
        "tasks": tasks,
        "pagination": {
            "page": page,
            "limit": records_per_page,
            "count": len(tasks),
            "total": total_records,
            "total_pages": math.ceil(total_records / records_per_page) if records_per_page else 1
        }
    }

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