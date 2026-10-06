from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Schema for creating a new todo item.

    Attributes:
        title: The text of the todo task.
        complete_by: Optional deadline date for the task.
    """

    title: str
    complete_by: Optional[date] = None


class TodoUpdate(BaseModel):
    """Schema for updating a todo item.

    Attributes:
        completed: The new completion status.
        complete_by: Optional updated deadline date.
    """

    completed: bool
    complete_by: Optional[date] = None


class TodoResponse(BaseModel):
    """Schema for returning a todo item in API responses.

    Attributes:
        id: The primary key of the todo.
        title: The text of the todo task.
        completed: Whether the task is complete.
        complete_by: Optional deadline date.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    complete_by: Optional[date] = None
