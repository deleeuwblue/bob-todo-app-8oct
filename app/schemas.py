from typing import Optional
from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Payload schema for creating a new todo item."""
    title: str
    due_date: Optional[str] = None


class TodoUpdate(BaseModel):
    """Payload schema for updating an existing todo item."""
    completed: Optional[bool] = None
    due_date: Optional[str] = None


class TodoResponse(BaseModel):
    """Response schema representing a todo item."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    due_date: Optional[str] = None
