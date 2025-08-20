from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    task_id: UUID = Field(default_factory=lambda: uuid4())
    descr: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    status: Optional[str]
