from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Schema for creating a new todo item.

    Attributes:
        title: The task description.
        due_date: Optional target completion date.
    """

    title: str
    due_date: Optional[date] = None


class TodoUpdate(BaseModel):
    """Schema for updating a todo item's completion status.

    Attributes:
        completed: Whether the task is completed.
    """

    completed: bool


class TodoResponse(BaseModel):
    """Schema for the todo item returned in API responses.

    Attributes:
        id: The primary key.
        title: The task description.
        completed: Whether the task is completed.
        due_date: Optional target completion date.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    due_date: Optional[date] = None
