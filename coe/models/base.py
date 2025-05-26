from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, func
from pydantic import BaseModel
from coe.utils.format_utils import to_camel

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

class CamelModel(BaseModel):
    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
        "from_attributes": True, 
    }