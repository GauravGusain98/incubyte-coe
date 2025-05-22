from pydantic import BaseModel, Field, constr, conint, field_validator
from typing import Optional, List
from enum import Enum
from datetime import date, datetime

NameStr = constr(strip_whitespace=True, min_length=1, max_length=128)
TextStr = constr(strip_whitespace=True, min_length=0, max_length=20000)
PasswordStr = constr(min_length=8, max_length=128)
ID = conint(gt=0)

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class PaginationSchema(BaseModel):
    page: int
    limit: int
    count: int
    total: int
    total_pages: int

### Request Schemas

class TaskFilters(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    search: Optional[str] = None

class CreateTaskRequestSchema(BaseModel):
    name: NameStr = Field(..., description="First name of the task")
    description: str = Field(..., description="Description of the task")
    assignee_id: Optional[ID] = None
    due_date: date
    start_date: Optional[date] = None
    priority: Optional[PriorityEnum] = None

class UpdateTaskRequestSchema(BaseModel):
    name: Optional[NameStr] = Field(default=None)
    description: Optional[str] = Field(default=None)
    assignee_id: Optional[ID]
    due_date: Optional[date] = Field(default=None)
    start_date: Optional[date]
    priority: Optional[PriorityEnum] = None

    @field_validator('name', 'description', 'due_date', mode='before')
    @classmethod
    def not_none_if_present(cls, value, field):
        print(field)
        if value is None:
            # Raise error only if the field was actually passed with value null
            raise ValueError(f"{field.field_name} cannot be null")
        return value

### Response Schemas
class CreateTaskResponseSchema(BaseModel):
    message: str
    task_id: int

class UpdateTaskResponseSchema(BaseModel):
    message: str

class GetTaskResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    created_by_id: int
    assignee_id: Optional[int] = None
    due_date: date
    start_date: Optional[date] = None
    priority: PriorityEnum
    created_at: datetime
    updated_on: Optional[datetime]

class GetTaskListResponseSchema(BaseModel):
    message: str
    tasks: List[GetTaskResponseSchema]
    pagination: PaginationSchema

class UpdateTaskResponseSchema(BaseModel):
    message: str

class DeleteTaskResponseSchema(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str