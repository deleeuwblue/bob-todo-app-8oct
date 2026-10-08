from datetime import date
from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Schema for creating a new todo item."""

    title: str
    due_date: date | None = None


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item."""

    completed: bool | None = None
    due_date: date | None = None


class TodoResponse(BaseModel):
    """Schema for returning a todo item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    due_date: date | None = None
